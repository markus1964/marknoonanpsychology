#!/usr/bin/env python3
"""Build assets/map-newport.png by stitching OpenStreetMap tiles around the clinic.

Run again if the address or framing changes:  python3 tools/make-map.py
Map data (c) OpenStreetMap contributors, ODbL. Attribution is shown on the page.
"""
import math, struct, urllib.request, zlib

LAT, LON = -37.8460074, 144.8725185     # 35 Challis Street, Newport VIC 3015
ZOOM = 16
OUT_W, OUT_H = 1200, 800
TILE = 256
UA = "MarkNoonanPsychologySiteBuild/1.0 (one-off static map generation)"


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
            if depth != 8 or colour not in (2, 3, 6):
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
    stride = w * channels
    prev = bytearray(stride)
    rows = []
    p = 0
    for _ in range(h):
        f = raw[p]; p += 1
        line = bytearray(raw[p:p + stride]); p += stride
        for i in range(stride):
            a = line[i - channels] if i >= channels else 0
            b = prev[i]
            c = prev[i - channels] if i >= channels else 0
            if f == 1:   line[i] = (line[i] + a) & 0xFF
            elif f == 2: line[i] = (line[i] + b) & 0xFF
            elif f == 3: line[i] = (line[i] + (a + b) // 2) & 0xFF
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                pred = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[i] = (line[i] + pred) & 0xFF
        prev = line

        if colour == 3:
            rows.append(bytes(b for idx in line for b in pal[idx * 3:idx * 3 + 3]))
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


cx, cy = project(LAT, LON, ZOOM)
left, top = cx - OUT_W / 2, cy - OUT_H / 2
tx0, ty0 = int(left // TILE), int(top // TILE)
tx1, ty1 = int((left + OUT_W) // TILE), int((top + OUT_H) // TILE)

canvas_w = (tx1 - tx0 + 1) * TILE
canvas = [bytearray(canvas_w * 3) for _ in range((ty1 - ty0 + 1) * TILE)]

for tx in range(tx0, tx1 + 1):
    for ty in range(ty0, ty1 + 1):
        url = "https://tile.openstreetmap.org/%d/%d/%d.png" % (ZOOM, tx, ty)
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            tw, th, rows = decode_png(r.read())
        ox, oy = (tx - tx0) * TILE, (ty - ty0) * TILE
        for j, row in enumerate(rows):
            canvas[oy + j][ox * 3:(ox + tw) * 3] = row
        print("tile", tx, ty, "ok")

sx, sy = int(left) - tx0 * TILE, int(top) - ty0 * TILE
crop = [bytes(canvas[sy + j][sx * 3:(sx + OUT_W) * 3]) for j in range(OUT_H)]
open("assets/map-newport.png", "wb").write(encode_png(OUT_W, OUT_H, crop))
print("wrote assets/map-newport.png", OUT_W, "x", OUT_H)
