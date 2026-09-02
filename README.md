# Adelaide Confident Driving Academy

Static marketing site for Adelaide Confident Driving Academy, formerly trading as
Adelaide Driver Training Academy SA. Plain HTML, CSS and JavaScript. No build
dependencies, no framework, no npm install.

Built by Nunik Co.

---

## Before you go live

Four things need doing. Nothing else is blocking.

### 1. Set the real domain

`content.py` line 16:

```python
SITE_URL = "https://adelaideconfidentdriving.com.au"
```

This one value feeds every canonical tag, Open Graph URL, sitemap entry and the
JSON-LD graph. Change it, run `python3 build.py`, commit.

### 2. Add Gopi's photos

Drop the files into `assets/img/team/` using exactly these names:

| File | Crop | Used on |
|---|---|---|
| `gopi-portrait.jpg` | Portrait, about 800 x 1000 | Home and About, main frame |
| `gopi-car-1.jpg` | Square, about 400 x 400 | Photo strip |
| `gopi-lesson-1.jpg` | Square, about 400 x 400 | Photo strip |
| `gopi-student-pass.jpg` | Square, about 400 x 400 | Photo strip |

Run `python3 build.py`. The placeholders are replaced automatically, alt text and
`loading="lazy"` included. If a file is missing, that slot keeps its placeholder
rather than breaking the layout.

Compress them first. Something like `cwebp` or Squoosh, aiming under 150 KB each.
Filenames must match exactly, including the `.jpg` extension. If you have `.png`
or `.webp` files, either rename them or change the filenames in the `PHOTOS` dict
in `content.py`.

### 3. Confirm the pricing with Gopi

Every figure in `content.py` under `PRICING` was carried across from the old site
as at September 2026. Confirm each one before launch. They appear on `/pricing/`,
on each service page, in the `Offer` structured data and in `llms.txt`, all
generated from that one dict.

### 4. Set up the redirects from the old domain

See the section below.

---

## Building

```bash
python3 build.py
```

Standard library only. Regenerates every HTML page plus `sitemap.xml`,
`robots.txt`, `llms.txt`, `llms-full.txt`, `site.webmanifest`, `vercel.json`,
`_headers` and `_redirects`.

Preview locally:

```bash
python3 -m http.server 8099
```

Then open http://127.0.0.1:8099. Note that clean URLs like `/pricing/` work
because of the `index.html` files, so the local preview matches production.

---

## How it fits together

```
content.py       Every word, price, review, suburb and FAQ. Edit this.
build.py         Templates and the generator. Edit for structure changes.
assets/css/      One stylesheet, tokenised, no framework.
assets/js/       One script. Preloader, nav, reveals, review filter, booking funnel.
assets/img/      Logo derivatives, icons, OG card. team/ is for Gopi's photos.
*.html           Generated. Do not edit by hand, your changes get overwritten.
```

The rule: **content changes go in `content.py`, layout changes go in `build.py`,
nothing gets hand-edited in the generated HTML.**

### Common edits

| To change | Edit |
|---|---|
| A price | `PRICING` in `content.py` |
| Add a review | `REVIEWS` in `content.py` (add its tag to `REVIEW_TAGS` if new) |
| Add a suburb | `AREAS` in `content.py` |
| Add an FAQ | `FAQS`, or a service's own `faqs` list |
| Phone or email | `PHONE_DISPLAY` / `PHONE_TEL` / `WA_NUMBER` / `EMAIL` |
| Add a service page | Append to `SERVICES`; the page, nav, sitemap and schema follow |
| WhatsApp number | `WA_NUMBER` in `content.py` **and** `WA_NUMBER` in `assets/js/site.js` |

That last one is the only value duplicated in two places. The Python side builds
the static links; the JavaScript side builds the funnel's dynamic link. Change
both together.

---

## Deployment

Static files. Push to git, connect the repo to Vercel, point Cloudflare DNS at it.

**Vercel:** no build command, no output directory, no framework preset. Serve the
repo root. `vercel.json` handles clean URLs, trailing slashes, the 301s, security
headers and cache policy.

**Cloudflare:** if you serve from Pages instead, `_headers` and `_redirects` carry
the same rules. Both files are generated from the same `REDIRECT_MAP` in
`build.py`, so they cannot drift.

If you put Cloudflare proxy in front of Vercel, set SSL/TLS to **Full (strict)**.
Leave Auto Minify off, the assets are already tight and it can break the inline
SVG.

### Redirecting the old domain

`adelaidedrivertrainingacademysa.com.au` has been indexed since 2006 and holds
whatever authority the business has built. Do not let it 404.

1. Keep the old domain registered and pointed somewhere you control.
2. Add it to the same Vercel project as a domain, then set it to redirect to the
   new domain. Vercel does this per-domain in the project's Domains settings.
3. `vercel.json` already maps the old paths:

   | Old | New |
   |---|---|
   | `/cbta-training-and-assessment/` | `/services/cbta-logbook-training/` |
   | `/vort-exam-training/` | `/services/vort-test-preparation/` |
   | `/about/` | `/about/` (unchanged) |
   | `/contact-us/` | `/contact/` |

   Every redirect is a 301. Anything unmatched lands on the 404 page, which is
   written for exactly this situation and points people back at the main pages.

4. In Google Search Console, verify both properties and submit a **Change of
   Address** from the old domain to the new one. This is the step people skip and
   it is the one that actually moves the ranking across.
5. Update the Google Business Profile website field to the new domain. Do this
   the same day you launch, since it is a strong local ranking signal.
6. Leave the redirects in place for at least a year. There is no benefit to
   removing them.

---

## SEO notes

**Structured data.** Every page carries a JSON-LD `@graph`. `DrivingSchool` and
`LocalBusiness` with `AggregateRating` (5.0 from 72), the eight reviews as
`Review` nodes, `Person` for Gopi, `Service` with `Offer` pricing on each service
page, `FAQPage` where there are FAQs, and `BreadcrumbList` throughout. Validate at
https://validator.schema.org and https://search.google.com/test/rich-results after
the domain is live.

**A caution on review markup.** Google's guidelines say self-serving review
markup should reflect genuine reviews collected by the business. These are real
Google reviews reproduced verbatim, which is defensible, but Google sometimes
discounts `Review` markup on a business's own site. The `AggregateRating` is the
part that matters most and it is accurate. If Search Console ever flags it, drop
the `review` array from `ld_business()` in `build.py` and keep the rest.

**AI and answer engines.** `robots.txt` explicitly allows GPTBot, ClaudeBot,
PerplexityBot, Applebot and the rest. `llms.txt` gives a structured summary and
`llms-full.txt` carries the complete content as clean markdown. Driving school
enquiries increasingly start in a chatbot, and the CBT&A versus VORT distinction
is exactly the kind of thing an assistant gets wrong without a clean source. Both
files spell it out.

**Keyword mapping.** One primary target per page, no cannibalisation:

| Page | Primary target |
|---|---|
| `/` | driving lessons Adelaide, driving school Adelaide |
| `/services/cbta-logbook-training/` | CBT&A Adelaide, logbook driving lessons SA |
| `/services/vort-test-preparation/` | VORT test Adelaide, mock driving test Adelaide |
| `/services/overseas-licence-conversion/` | overseas licence conversion Adelaide |
| `/services/beginner-driving-lessons/` | nervous driver lessons Adelaide |
| `/services/refresher-driving-lessons/` | refresher driving lessons Adelaide |
| `/pricing/` | driving lesson prices Adelaide, how much are driving lessons Adelaide |
| `/service-areas/` | driving lessons near me, driving instructor \[suburb\] |
| `/about/` | Gopi driving instructor Adelaide |
| `/reviews/` | best driving instructor Adelaide |

**What to do after launch.**

1. Submit `sitemap.xml` in Google Search Console and Bing Webmaster Tools.
2. File the Change of Address from the old domain.
3. Update the Google Business Profile website URL.
4. Add the business to Yellow Pages, Hotfrog, Localsearch and TrueLocal with
   identical name, address and phone. NAP consistency is most of local SEO.
5. Ask new students for Google reviews. It is still the single biggest lever for
   a service-area business, well ahead of anything on the site itself.
6. Consider suburb landing pages later (`/driving-lessons-salisbury/` and so on)
   if the four regional sections are not ranking. Only do this with genuinely
   different content per suburb, otherwise it is thin-content spam and will hurt.

---

## Accessibility

WCAG 2.1 AA was the target and the build was checked against it.

- Every text and background pairing clears 4.5:1. The primary button uses `#2563EB`
  rather than the brighter `#3A86FF` for exactly this reason: white on `#3A86FF`
  is only 3.48:1. The bright cobalt stays for borders, focus rings and progress bars
  where it is decorative.
- Skip link, visible focus rings, one `h1` per page, no heading level skips.
- Tap targets are at least 44 x 44, most are 52.
- `prefers-reduced-motion` disables the preloader, scroll reveals, counters and
  every transition.
- The booking funnel uses real `fieldset` and `legend` elements, radio inputs
  rather than divs, `role="alert"` on the error message and `role="status"` on the
  confirmation. It works with a keyboard alone.
- Nothing depends on JavaScript to be readable. With JS off you get the full site,
  static WhatsApp and phone links, and no funnel.

---

## Browser support

Evergreen Chrome, Safari, Firefox and Edge. The JavaScript is ES5 with no
transpilation needed. `backdrop-filter` degrades to a solid background where
unsupported. `IntersectionObserver` is feature-detected and falls back to showing
everything immediately.

---

## Things deliberately left out

- **No contact form.** WhatsApp and phone convert far better for this business and
  a form means spam, a backend and a privacy policy obligation. If one is ever
  wanted, use Formspree or Vercel Forms rather than adding a server.
- **No analytics.** Add Plausible or Fathom if you want numbers. Both are one
  script tag and neither needs a cookie banner. Google Analytics would need a
  consent banner and a privacy policy under Australian Privacy Act guidance.
- **No cookies at all.** The site sets none, which is why there is no consent
  banner. Keep it that way if you can.
- **No CMS.** `content.py` is the CMS. If Gopi needs to edit content himself,
  Decap CMS over the git repo would be the lightest option.

---

## Licence and credits

Content and branding belong to Adelaide Confident Driving Academy. Logo supplied
by the client; the transparent, light-knockout, favicon and Open Graph derivatives
were generated from it and live in `assets/img/`.
