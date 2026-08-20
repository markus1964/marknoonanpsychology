#!/usr/bin/env python3
"""Build the light and dark map images by stitching CARTO basemap tiles around the clinic.

Writes assets/map-newport.png and assets/map-newport-dark.png.
Run again if the address or framing changes:  python3 tools/make-map.py

Tiles from CARTO basemaps, map data (c) OpenStreetMap contributors.
Both are credited under the map on the page, as their licences require.
"""
import math, struct, urllib.request, zlib

LAT, LON = -37.8460074, 144.8725185     # 35 Challis Street, Newport VIC 3015
ZOOM = 15

# Zoom 15 rather than 16: at this display size 16 is too tight to show where
# Newport actually is, and 15 still keeps the street names readable.
# The map is displayed about 440 CSS pixels wide. Rendering far more than that
# and letting the browser shrink it is what made the labels illegible, so the
# output is sized to the display box at 2x using CARTO's retina tiles, which
# draw their labels at 2x to match. Result: sharp on retina, correct label size.
OUT_W, OUT_H = 880, 587
TILE = 512
RETINA = "@2x"
UA = "MarkNoonanPsychologySiteBuild/1.0 (one-off static map generation)"

# CARTO basemaps, chosen over the default OpenStreetMap style because the two
# variants are a matched pair and the muted palette suits the site.
# CARTO's dark style is drawn for full-bleed backgrounds and is unreadably dim
# inside a small framed panel. Sampling a tile shows the whole style squeezed
# into the bottom of the range: land sits at 8, roads at 25, labels between 30
# and 60, and almost nothing above that. The dark variant therefore gets a curve
# that stretches that narrow band across a usable range, holding the land close
# to the page background while pushing roads and labels up until they read.
STYLES = {
    "assets/map-newport.png": ("light_all", False),
    "assets/map-newport-dark.png": ("dark_all", True),
}
INK_MAX = 60      # everything meaningful in the source sits below this
GROUND = 18       # darkest output, near the page background
LABEL = 200       # where INK_MAX lands, so labels read clearly
KNEE = 1.35       # >1 holds the land down while still lifting roads


def project(lat, lon, z):
    n = 2 ** z
    x = (lon + 180.0) / 360.0 * n
    y = (1.0 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2.0 * n
    return x * TILE, y * TILE


def decode_png(data):
    """Minimal PNG reader for the colour types OSM tiles actually use. Returns (w, h, rgb rows)."""
    pos, idat, pal, trns = 8, b"", None, None
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        kind = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        pos += 12 + length
        if kind == b"IHDR":
            w, h, depth, colour = struct.unpack(">IIBB", body[:10])
            if colour not in (2, 3, 6) or depth not in (1, 2, 4, 8):
                raise ValueError("unsupported PNG: depth %d colour %d" % (depth, colour))
            if colour != 3 and depth != 8:
                raise ValueError("unsupported PNG: depth %d colour %d" % (depth, colour))
        elif kind == b"PLTE":
            pal = body
        elif kind == b"tRNS":
            trns = body
        elif kind == b"IDAT":
            idat += body
        elif kind == b"IEND":
            break

    channels = {2: 3, 3: 1, 6: 4}[colour]
    raw = zlib.decompress(idat)
    # Sub-byte palette depths pack several pixels per byte; filtering still works
    # on whole bytes, so unfilter first and expand the indices afterwards.
    stride = (w * channels * depth + 7) // 8
    filter_bpp = max(1, channels * depth // 8)
    prev = bytearray(stride)
    rows = []
    p = 0
    for _ in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        for i in range(stride):
            a = line[i - filter_bpp] if i >= filter_bpp else 0
            b = prev[i]
            c = prev[i - filter_bpp] if i >= filter_bpp else 0
            if f == 1:   line[i] = (line[i] + a) & 0xFF
            elif f == 2: line[i] = (line[i] + b) & 0xFF
            elif f == 3: line[i] = (line[i] + (a + b) // 2) & 0xFF
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        prev = line

        if colour == 3:
            if depth == 8:
                idx = line
            else:
                per = 8 // depth
                mask = (1 << depth) - 1
                idx = [(line[i // per] >> (8 - depth * (i % per + 1))) & mask
                       for i in range(w)]
            rows.append(bytes(b for i in idx for b in pal[i * 3:i * 3 + 3]))
        elif colour == 6:
            rows.append(bytes(v for i in range(0, stride, 4) for v in line[i:i + 3]))
        else:
            rows.append(bytes(line))
    return w, h, rows


def encode_png(w, h, rows):
    raw = b"".join(b"\x00" + r for r in rows)
    def chunk(kind, body):
        c = kind + body
        return struct.pack(">I", len(body)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def tone_curve():
    """256-entry lookup, applied with bytes.translate to stay fast in pure Python."""
    table = bytearray(256)
    for v in range(256):
        if v <= INK_MAX:
            x = (v / INK_MAX) ** KNEE
            table[v] = int(GROUND + (LABEL - GROUND) * x)
        else:
            x = (v - INK_MAX) / (255 - INK_MAX)
            table[v] = int(LABEL + (255 - LABEL) * x)
    return bytes(table)


def build(out_path, style, lift):
    cx, cy = project(LAT, LON, ZOOM)
    left, top = cx - OUT_W / 2, cy - OUT_H / 2
    tx0, ty0 = int(left // TILE), int(top // TILE)
    tx1, ty1 = int((left + OUT_W) // TILE), int((top + OUT_H) // TILE)

    canvas_w = (tx1 - tx0 + 1) * TILE
    canvas = [bytearray(canvas_w * 3) for _ in range((ty1 - ty0 + 1) * TILE)]

    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            url = "https://basemaps.cartocdn.com/%s/%d/%d/%d%s.png" % (style, ZOOM, tx, ty, RETINA)
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                tw, th, rows = decode_png(r.read())
            ox, oy = (tx - tx0) * TILE, (ty - ty0) * TILE
            for j, row in enumerate(rows):
                canvas[oy + j][ox * 3:(ox + tw) * 3] = row

    sx, sy = int(left) - tx0 * TILE, int(top) - ty0 * TILE
    crop = [bytes(canvas[sy + j][sx * 3:(sx + OUT_W) * 3]) for j in range(OUT_H)]
    if lift:
        lut = tone_curve()
        crop = [row.translate(lut) for row in crop]
    open(out_path, "wb").write(encode_png(OUT_W, OUT_H, crop))
    print("wrote", out_path, OUT_W, "x", OUT_H)


for path, (style, lift) in STYLES.items():
    build(path, style, lift)
