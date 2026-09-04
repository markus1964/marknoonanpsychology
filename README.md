# Mark Noonan Psychology: your website

This folder holds your whole website. There are no programs to install and nothing to sign up for to look at it.

---

## Looking at the site on your computer

**Double-click `index.html`.** It opens in your web browser and works exactly as it will once it is online.

That is the whole trick. Nothing needs to be running, and you can do this as often as you like without breaking anything. If it opens in the wrong program, right-click the file, choose **Open With**, and pick Safari or Chrome.

The web address in the browser bar will look like `file:///Users/...` rather than your real domain. That is normal and only happens on your own computer.

---

## Before it goes live

### Get a separate work number

Right now the site publishes **0411 477 292**, which I understand is your personal mobile. Once the site is online, that number is public and gets copied by automated systems that scrape websites. You cannot really undo that later.

It is worth setting up a second number just for the practice:

- **An eSIM** is a second phone line on the same physical phone, no second handset needed. Most Australian carriers sell them, they cost a few dollars a month, and your phone shows both numbers separately. You can silence the work line outside your consulting hours.
- **A VoIP number** (Skype, Google Voice, or an Australian provider like MyNetFone) works similarly and rings through an app.

Either way you get a number you can hand out freely, put on a business card, silence on a Sunday, and pass to someone else if your practice ever changes shape. Your personal number stays personal.

If you set one up, tell me before the site goes live and I will swap it in. It appears in a few places behind the scenes, so it is better done once, before the number gets indexed by Google.

### Two bits of writing that are mine, not yours

Almost every word on the site is yours, just reordered. Two blocks are not, and I would like you to correct them or cut them:

1. **The "Getting started" section**, the three numbered steps about first contact, a short conversation, and the first session. I wrote these because people deciding whether to email a psychologist are usually most anxious about what happens next. But they describe how *you* work, so the words should be yours.
2. **The two therapy explanations.** On the site, "ACT" and "attachment" in the "My approach" section can be clicked, and a short plain-English description appears. I drafted those descriptions from published sources. You may well explain them differently to your own clients.

Read both on the site, mark up anything that is not how you would put it, and send it back.

---

## Changing the words later

All the text lives in the file `index.html`. It is a plain text file with the website's words scattered among formatting codes. It looks alarming at first, but the words themselves are in ordinary English and you can safely change them if you are careful not to delete the pointy brackets around them.

**On a Mac, do this once first**, or TextEdit will quietly ruin the file:

1. Open TextEdit.
2. Menu bar: **TextEdit → Settings → Open and Save**.
3. Tick **"Display HTML files as HTML code instead of formatted text"**.

Then you can open `index.html` in TextEdit and edit it. Keep a copy of the file before you start, so there is something to go back to.

Honestly though: send me the changes and I will make them. It takes me two minutes and there is no risk of a stray keystroke breaking the page.

Things you are most likely to want changed:

- **Your fee**, currently "$220 per session (before Medicare rebate)"
- **Your hours**, currently "Fridays, 9am to 5pm"
- **Your photo.** Save the new one as `mark.jpg` in the `assets` folder, replacing the one there. It should be a portrait shape, taller than it is wide. Tell me when you have, because the image that shows up when someone shares your website on Facebook or in a text message uses the same photo and needs rebuilding.

---

## Putting the site online

You need two things: somewhere to host the files, and your domain pointed at it. Hosting is free. You already own the domain.

These steps use GitHub, which is free and does not require you to install anything or use any commands. You will be uploading files through a normal web page.

### Step 1: Make a free GitHub account

Go to [github.com](https://github.com) and sign up. Any email address works. Choose any username, it does not need to be professional, but you will type it again in step 5, so write it down.

### Step 2: Make a place for the files

1. Once logged in, click the **+** in the top right, then **New repository**.
2. Under **Repository name**, type: `marknoonanpsychology`
3. Leave everything else alone, but make sure **Public** is selected. It must be public for the free hosting to work. This does not make anything private visible, it just means the website's files can be read, which is what a website is.
4. Click **Create repository**.

### Step 3: Upload the website

1. On the page that appears, find and click **uploading an existing file**.
2. Open this folder on your computer, select everything in it, and drag it all onto the GitHub page.
3. Wait for the uploads to finish, then click **Commit changes** at the bottom.

### Step 4: Turn the website on

1. Click **Settings** at the top of your repository, then **Pages** in the left-hand menu.
2. Under **Source**, choose **Deploy from a branch**.
3. Set the branch to **main** and the folder to **/ (root)**, then click **Save**.

Wait a couple of minutes. Your site is now live at a temporary address that GitHub shows you on that page. Have a look and check it is all there.

### Step 5: Point your domain at it

This part happens wherever you bought `marknoonanpsychology.com.au`, not on GitHub. Log in there and find the DNS settings, sometimes called "DNS records" or "Advanced DNS".

Add these five records:

| Type  | Name / Host | Value                       |
|-------|-------------|-----------------------------|
| A     | @           | 185.199.108.153             |
| A     | @           | 185.199.109.153             |
| A     | @           | 185.199.110.153             |
| A     | @           | 185.199.111.153             |
| CNAME | www         | YOURUSERNAME.github.io      |

Replace `YOURUSERNAME` with the GitHub username from step 1. Keep the full stop at the end of `github.io` if your provider adds one.

If this screen looks daunting, most registrars will do it for you if you send them that table and ask them to point the domain at GitHub Pages.

### Step 6: Wait, then switch on the padlock

DNS changes take anywhere from a few minutes to a day to spread across the internet. Once `marknoonanpsychology.com.au` shows your site, go back to **Settings → Pages** on GitHub and tick **Enforce HTTPS**. That gives you the padlock in the browser bar. It is free and automatic, but the tickbox only appears once the domain is working.

---

## Getting found on Google

The site is already built so Google can read it properly: it describes who you are, where you consult, your hours, your fee and your areas of practice in the hidden format search engines look for. That part is done.

Two things still need doing by hand, and they matter more than anything on the page itself:

### Google Business Profile, do this first

Go to [business.google.com](https://business.google.com) and create a profile for the practice at the TreeHaus address. This is what puts you in the map results when someone searches "psychologist Newport", and for a local practice it will bring in more enquiries than the website will.

Google verifies the address by posting a code to it, which takes a week or two, so start it early. You will need TreeHaus to be comfortable with you listing their address.

### Nearby suburbs

Under the map, the site names the suburbs around Newport in an ordinary sentence, and the hidden data lists them properly. That is the honest version of what some clinics do by stuffing suburb names into invisible text, which Google penalises. If there is a suburb you actually draw clients from and I have missed it, tell me and I will add it.

### Google Search Console

Go to [search.google.com/search-console](https://search.google.com/search-console), add `marknoonanpsychology.com.au`, and follow the verification steps. Then submit `https://marknoonanpsychology.com.au/sitemap.xml` when it asks for a sitemap. This tells Google the site exists rather than waiting to be found, and shows you what people searched for to reach you.

A realistic expectation: a brand new website competes against clinics that have been online for years. The site gives you a solid foundation, but the Business Profile and your existing referral relationships will do the heavy lifting for the first few months.

---

## A few honest notes

- **There is no contact form on purpose.** People phone or email you directly. That means no third-party company ever handles a message from someone about their mental health, which felt like the right call for a psychology practice.
- **The "Make an enquiry" button** opens the visitor's email with a short template already written, so they are not staring at an empty message wondering what to say.
- **The map** is a picture, not a Google map. It loads instantly, does not track your visitors, and links through to directions when clicked. There are two versions, light and dark, and the site shows whichever matches the visitor's setting. Only the one being used is downloaded.
- **Light and dark.** The site follows whatever the visitor's phone or computer is set to. The small circle at the top right lets them switch.
- **No tracking, no cookies, no analytics.** Nothing is collected about anyone who visits.

---

## For a developer

Plain HTML and CSS, no build step, no dependencies, no framework. `index.html`, `styles.css`, `site.js`, plus `assets/`.

- Theming is a single set of CSS custom properties at the top of `styles.css`, redefined under `prefers-color-scheme: dark` and `[data-theme="dark"]`. The toggle writes to `localStorage`.
- `assets/map-newport.png` and `assets/map-newport-dark.png` are stitched from CARTO basemap tiles by `tools/make-map.py`, which writes both in one run. The map is a CSS background driven by the `--map` custom property rather than an `<img>`, so only the current theme's file is fetched. OpenStreetMap and CARTO are both credited under the map as their licences require. Re-run the script if the address changes.
- Two things make the map legible and are easy to undo by accident. It is rendered at 880x587 to match its roughly 440px display box at 2x, using CARTO's `@2x` tiles so labels are drawn at retina size; rendering a larger image and letting the browser shrink it makes the street names unreadable. And the dark tiles get a tone curve, because CARTO's dark style squeezes land, roads and labels into values 8 to 60 and is far too dim inside a small panel. Constants and reasoning are in the script.
- Google Maps imagery is deliberately not used. Screenshotting Google Maps and hosting the result breaches their terms; the licensed route is the Static Maps API, which needs an API key with billing enabled.
- `assets/og-card.jpg` (1200x630 social share card) is rendered from `tools/og-card.html`; the rebuild command is a comment at the top of that file. Rebuild whenever the photo, name or tagline changes.
- The two modality terms in "My approach" are `<button>` elements with `aria-expanded`/`aria-controls` driving sibling `.term-panel` divs. One open at a time, all closed on load.
- No Medicare rebate amount is published deliberately, since the Government indexes rebates every 1 July and any figure would silently go stale. The relevant item is 80110 on [MBS Online](https://www9.health.gov.au/mbs/fullDisplay.cfm?type=item&q=80110) if that decision is ever revisited.
- `CNAME` holds the apex domain for GitHub Pages. `sitemap.xml` has a `lastmod` worth bumping on meaningful content changes.
- Cloudflare Pages is a drop-in alternative: connect the repo, no build command, output directory `/`.
