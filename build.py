#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Static site generator for Adelaide Confident Driving Academy.

    python3 build.py

No dependencies beyond the standard library. Writes plain HTML into the repo
root so the output can be served by anything: Vercel, Cloudflare Pages,
Netlify, or a bucket.
"""

import html
import json
import os
import re
import shutil
from datetime import date

import content as C

ROOT = os.path.dirname(os.path.abspath(__file__))
TODAY = date.today().isoformat()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def e(s):
    """Escape for HTML text nodes and attributes."""
    return html.escape(str(s), quote=True)


def url(path):
    """Absolute URL from a site-root path."""
    return C.SITE_URL.rstrip("/") + path


def wa_link(message):
    """A wa.me link with a URL-encoded pre-filled message."""
    from urllib.parse import quote
    return "https://wa.me/%s?text=%s" % (C.WA_NUMBER, quote(message, safe=""))


def initials(name):
    parts = [p for p in re.split(r"\s+", name.strip()) if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


def photo_exists(filename):
    return os.path.isfile(os.path.join(ROOT, "assets", "img", "team", filename))


ICONS = {
    "logbook": '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H19a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H6.5a1.5 1.5 0 0 0 0 3H20a1 1 0 1 1 0 2H6.5A3.5 3.5 0 0 1 3 19.5v-15Zm4 2.5a1 1 0 0 0 0 2h8a1 1 0 1 0 0-2H8Zm0 4a1 1 0 1 0 0 2h5a1 1 0 1 0 0-2H8Z"/>',
    "target": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 3a7 7 0 1 1 0 14 7 7 0 0 1 0-14Zm0 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8Zm0 2.5a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3Z"/>',
    "globe": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20ZM4.06 13h3.02c.1 1.72.45 3.32.98 4.6A8.02 8.02 0 0 1 4.06 13Zm3.02-2H4.06a8.02 8.02 0 0 1 4-4.6c-.53 1.28-.88 2.88-.98 4.6Zm2 0c.13-2.04.6-3.74 1.2-4.78.24-.4.47-.68.66-.85V11H9.08Zm3.86 0V5.37c.19.17.42.45.66.85.6 1.04 1.07 2.74 1.2 4.78h-1.86Zm0 2h1.86c-.13 2.04-.6 3.74-1.2 4.78-.24.4-.47.68-.66.85V13Zm-2 0v5.63c-.19-.17-.42-.45-.66-.85-.6-1.04-1.07-2.74-1.2-4.78h1.86Zm5.9 0h3.02a8.02 8.02 0 0 1-4 4.6c.53-1.28.88-2.88.98-4.6Zm0-2c-.1-1.72-.45-3.32-.98-4.6a8.02 8.02 0 0 1 4 4.6h-3.02Z"/>',
    "heart": '<path d="M12 21s-7.5-4.6-9.5-9A5.5 5.5 0 0 1 12 6.5 5.5 5.5 0 0 1 21.5 12c-2 4.4-9.5 9-9.5 9Z"/>',
    "refresh": '<path d="M12 4a8 8 0 0 1 7.2 4.5l1.9-.9A10 10 0 0 0 12 2a10 10 0 0 0-9.6 7.2L1 6.5V13h6.5l-2.6-2.1A8 8 0 0 1 12 4Zm10 7h-6.5l2.6 2.1A8 8 0 0 1 4.8 15.5l-1.9.9A10 10 0 0 0 12 22a10 10 0 0 0 9.6-7.2l1.4 2.7V11Z"/>',
    "phone": '<path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25c1.1.37 2.3.57 3.6.57a1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1l-2.22 2.23Z"/>',
    "mail": '<path d="M2 6a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V6Zm2.5.5L12 12l7.5-5.5H4.5Z"/>',
    "pin": '<path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/>',
    "clock": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm1 5h-2v6l4.6 2.8 1-1.7-3.6-2.1V7Z"/>',
    "star": '<path d="m12 2 2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.2 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8L12 2Z"/>',
}


def icon(name, size=24):
    path = ICONS.get(name, ICONS["star"])
    return ('<svg aria-hidden="true" width="%d" height="%d" viewBox="0 0 24 24" '
            'fill="currentColor">%s</svg>' % (size, size, path))


WA_SVG = ('<svg aria-hidden="true" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">'
          '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38'
          'a9.87 9.87 0 0 0 4.79 1.22h.01c5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2Zm5.8 14.17'
          'c-.24.68-1.4 1.3-1.95 1.35-.5.05-1.13.07-1.83-.11-.42-.11-.96-.29-1.65-.59-2.9-1.25'
          '-4.8-4.17-4.94-4.36-.15-.19-1.19-1.58-1.19-3.02s.76-2.14 1.03-2.44c.27-.29.58-.37.78'
          '-.37h.56c.18 0 .42-.07.66.5.24.59.83 2.03.9 2.18.07.15.12.32.02.51-.09.19-.14.31-.28'
          '.48-.14.17-.29.37-.42.5-.14.14-.28.29-.12.57.16.29.71 1.17 1.53 1.9 1.05.94 1.94 1.23 '
          '2.22 1.37.27.14.43.12.59-.07.16-.19.68-.79.86-1.07.18-.27.36-.22.61-.13.24.09 1.55.73 '
          '1.82.86.27.14.44.2.5.32.07.11.07.65-.17 1.33Z"/></svg>')

STARS = '<span class="stars" aria-hidden="true">★★★★★</span>'


def chip_class(svc, default):
    """Plate-colour chip for the two licence pathways; everything else keeps its
    existing colour (cobalt/gold), so the plate code stays meaningful."""
    plate = svc.get("plate")
    if plate == "yellow":
        return "chip chip--plate-yellow"
    if plate == "red":
        return "chip chip--plate-red"
    return "chip %s" % default


def glow_class(svc):
    plate = svc.get("plate")
    if plate == "yellow":
        return "card-glow--yellow"
    if plate == "red":
        return "card-glow--red"
    return "card-glow--cobalt"


def marquee_band(svc):
    """Full-bleed decorative keyword strip. aria-hidden: every keyword already
    exists in real body copy elsewhere on the page, this is reinforcement only."""
    words = svc["marquee"]
    glyph = '<span class="marquee-dot" aria-hidden="true">&#9670;</span>'
    track = glyph.join('<span>%s</span>' % e(w) for w in words)
    plate = svc.get("plate")
    band_class = "marquee--plate-yellow" if plate == "yellow" else \
                 "marquee--plate-red" if plate == "red" else "marquee--cobalt"
    return ("""<div class="marquee %(cls)s" aria-hidden="true">
  <div class="marquee-track">
    <span class="marquee-set">%(track)s%(glyph)s</span>
    <span class="marquee-set">%(track)s%(glyph)s</span>
  </div>
</div>""" % {"cls": band_class, "track": track, "glyph": glyph})


# ---------------------------------------------------------------------------
# Structured data
# ---------------------------------------------------------------------------

def ld_business():
    return {
        "@type": ["DrivingSchool", "LocalBusiness"],
        "@id": url("/#business"),
        "name": C.BRAND,
        "alternateName": [C.BRAND_SHORT, C.LEGAL_PREVIOUS, "ACDA"],
        "description": ("One-to-one driving school serving Adelaide and South Australia. "
                        "CBT&A logbook training, VORT test preparation, overseas licence "
                        "conversion and lessons for nervous beginners."),
        "url": C.SITE_URL + "/",
        "telephone": C.PHONE_TEL,
        "email": C.EMAIL,
        "foundingDate": C.FOUNDED,
        "image": url("/assets/img/og-default.png"),
        "logo": {"@type": "ImageObject", "url": url("/assets/img/icon-512.png"),
                 "width": 512, "height": 512},
        "priceRange": "$$",
        "currenciesAccepted": "AUD",
        "address": {"@type": "PostalAddress", "addressLocality": C.LOCALITY,
                    "addressRegion": C.POSTAL_REGION, "addressCountry": "AU"},
        "geo": {"@type": "GeoCoordinates", "latitude": C.GEO_LAT, "longitude": C.GEO_LNG},
        "areaServed": [{"@type": "City", "name": "Adelaide"}] +
                      [{"@type": "Place", "name": s} for a in C.AREAS for s in a["suburbs"]],
        "serviceArea": {
            "@type": "GeoCircle",
            "geoMidpoint": {"@type": "GeoCoordinates", "latitude": C.GEO_LAT, "longitude": C.GEO_LNG},
            "geoRadius": str(int(C.SERVICE_RADIUS_KM) * 1000),
        },
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                          "Saturday", "Sunday"],
            "opens": "07:00", "closes": "20:00",
        }],
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": C.RATING,
            "reviewCount": C.REVIEW_COUNT,
            "bestRating": "5", "worstRating": "1",
        },
        "review": [{
            "@type": "Review",
            "author": {"@type": "Person", "name": r["name"]},
            "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
            "reviewBody": r["text"],
        } for r in C.REVIEWS],
        "employee": {"@id": url("/about/#gopi")},
        "founder": {"@id": url("/about/#gopi")},
        "sameAs": [C.GOOGLE_PROFILE, C.GOOGLE_KG, C.OLD_DOMAIN],
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "Driving lessons and assessments",
            "itemListElement": [{
                "@type": "Offer",
                "itemOffered": {"@type": "Service", "name": s["nav"],
                                "url": url("/services/%s/" % s["slug"])},
            } for s in C.SERVICES],
        },
    }


def ld_person():
    return {
        "@type": "Person",
        "@id": url("/about/#gopi"),
        "name": C.INSTRUCTOR,
        "alternateName": C.INSTRUCTOR_FULL,
        "jobTitle": "Lead driving instructor and CBTA Certified Examiner",
        "worksFor": {"@id": url("/#business")},
        "knowsAbout": ["CBT&A Competency Based Training and Assessment",
                       "Vehicle On Road Test (VORT)",
                       "Overseas driver licence conversion in South Australia",
                       "Learner driver instruction", "Automobile engineering"],
        "description": ("Driving instructor in South Australia since 2006 with a background "
                        "in automobile engineering. Known for calm, patient one-to-one "
                        "instruction."),
    }


def ld_website():
    return {
        "@type": "WebSite",
        "@id": url("/#website"),
        "url": C.SITE_URL + "/",
        "name": C.BRAND,
        "inLanguage": "en-AU",
        "publisher": {"@id": url("/#business")},
    }


def ld_breadcrumbs(crumbs):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [{
            "@type": "ListItem", "position": i + 1, "name": name,
            "item": url(path),
        } for i, (name, path) in enumerate(crumbs)],
    }


def ld_faq(pairs):
    return {
        "@type": "FAQPage",
        "mainEntity": [{
            "@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a},
        } for q, a in pairs],
    }


def ld_service(svc):
    group = C.PRICING[svc["price_group"]]
    prices = [int(it["price"]) for it in group["items"]]
    offers = [{
        "@type": "Offer",
        "name": it["name"],
        "price": it["price"],
        "priceCurrency": "AUD",
        "availability": "https://schema.org/InStock",
        "url": url("/pricing/"),
        "description": it["desc"],
    } for it in group["items"]]
    return {
        "@type": "Service",
        "@id": url("/services/%s/#service" % svc["slug"]),
        "name": svc["nav"],
        "serviceType": svc["nav"],
        "description": svc["meta"],
        "provider": {"@id": url("/#business")},
        "areaServed": [{"@type": "City", "name": "Adelaide"}],
        "url": url("/services/%s/" % svc["slug"]),
        "offers": {
            "@type": "AggregateOffer",
            "priceCurrency": "AUD",
            "lowPrice": str(min(prices)),
            "highPrice": str(max(prices)),
            "offerCount": len(offers),
            "offers": offers,
        },
    }


def jsonld(*blocks):
    graph = {"@context": "https://schema.org", "@graph": list(blocks)}
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(graph, ensure_ascii=False, separators=(",", ":")))


# ---------------------------------------------------------------------------
# Shell
# ---------------------------------------------------------------------------

def head(page):
    """page: dict with path, title, meta, plus optional og_type, schema, noindex."""
    canonical = url(page["path"])
    og_img = url("/assets/img/og-default.png")
    robots = "noindex, follow" if page.get("noindex") else \
             "index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1"
    return """<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>%(title)s</title>
<meta name="description" content="%(meta)s">
<link rel="canonical" href="%(canonical)s">
<meta name="robots" content="%(robots)s">
<meta name="theme-color" content="#0B132B">
<meta name="author" content="%(brand)s">
<meta name="geo.region" content="AU-SA">
<meta name="geo.placename" content="Adelaide">
<meta name="geo.position" content="%(lat)s;%(lng)s">
<meta name="ICBM" content="%(lat)s, %(lng)s">

<meta property="og:site_name" content="%(brand)s">
<meta property="og:type" content="%(ogtype)s">
<meta property="og:locale" content="en_AU">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(meta)s">
<meta property="og:url" content="%(canonical)s">
<meta property="og:image" content="%(ogimg)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="%(brand)s, five star rated driving school in Adelaide">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="%(title)s">
<meta name="twitter:description" content="%(meta)s">
<meta name="twitter:image" content="%(ogimg)s">

<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<!-- Loaded normally rather than with a media=print/onload swap: the CSP forbids
     inline event handlers, and display=swap already prevents invisible text. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Outfit:wght@600;700;800&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
<script src="/assets/js/site.js" defer></script>
%(schema)s
</head>
<body>
""" % {
        "title": e(page["title"]), "meta": e(page["meta"]), "canonical": e(canonical),
        "robots": robots, "brand": e(C.BRAND), "ogtype": page.get("og_type", "website"),
        "ogimg": e(og_img), "schema": page.get("schema", ""),
        "lat": C.GEO_LAT, "lng": C.GEO_LNG,
    }


def preloader():
    return """<div id="preloader" role="status" aria-label="Loading">
  <div class="pl-inner">
    <img src="/assets/img/logo-mark-light.png" alt="" width="84" height="84">
    <div class="pl-name">Adelaide Confident</div>
    <div class="pl-sub">Driving Academy</div>
  </div>
</div>
"""


def header(active):
    links = "".join(
        '<li><a href="%s"%s>%s</a></li>' % (
            path, ' aria-current="page"' if active == path else "", e(label))
        for label, path in C.NAV)
    return """<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="/">
        <img src="/assets/img/logo-mark-light.png" alt="" width="42" height="42">
        <span class="brand-text">
          <b>Adelaide Confident</b>
          <span>Driving Academy</span>
        </span>
      </a>
      <ul class="nav-links" id="nav-links">%(links)s</ul>
      <div class="nav-cta">
        <a class="nav-call" href="tel:%(tel)s">%(phone_icon)s<span>%(phone)s</span></a>
        <a class="btn btn--whatsapp btn--sm" href="%(wa)s" rel="noopener">%(wa_icon)s Book now</a>
        <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav-links" aria-label="Menu"><span></span></button>
      </div>
    </nav>
  </div>
</header>
""" % {
        "links": links, "tel": C.PHONE_TEL, "phone": e(C.PHONE_DISPLAY),
        "phone_icon": icon("phone", 16), "wa_icon": WA_SVG,
        "wa": e(wa_link("Hi Gopi, I'd like to book a driving lesson with Adelaide Confident "
                        "Driving Academy. Could you let me know your availability?")),
    }


def footer():
    svc = "".join('<li><a href="/services/%s/">%s</a></li>' % (s["slug"], e(s["nav"]))
                  for s in C.SERVICES)
    areas = "".join('<li><a href="/service-areas/#%s">%s</a></li>' % (a["slug"], e(a["name"]))
                    for a in C.AREAS)
    res = "".join('<li><a href="%s" rel="noopener nofollow" target="_blank">%s</a></li>'
                  % (e(u), e(n)) for n, u in C.RESOURCES)
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="/">
          <img src="/assets/img/logo-mark-light.png" alt="" width="42" height="42">
          <span class="brand-text"><b>Adelaide Confident</b><span>Driving Academy</span></span>
        </a>
        <p>One-to-one driving lessons across Adelaide with %(inst)s. Teaching South Australians
        to drive since %(founded)s.</p>
        <div class="footer-contact">
          <a href="tel:%(tel)s">%(ic_phone)s %(phone)s</a>
          <a href="mailto:%(email)s">%(ic_mail)s %(email)s</a>
          <a href="%(wa)s" rel="noopener">%(wa_icon)s Message on WhatsApp</a>
        </div>
      </div>
      <div>
        <h4>Lessons</h4>
        <ul>%(svc)s<li><a href="/pricing/">Pricing</a></li></ul>
      </div>
      <div>
        <h4>Areas served</h4>
        <ul>%(areas)s</ul>
      </div>
      <div>
        <h4>Official resources</h4>
        <ul>%(res)s</ul>
      </div>
    </div>

    <div class="acknowledgement">
      <b>Acknowledgement of Country</b>
      %(ack)s
    </div>

    <div class="footer-base">
      <p>&copy; <span data-year>2026</span> %(brand)s. Formerly trading as %(prev)s.</p>
      <p>%(hours)s &middot; ABN available on request</p>
    </div>
  </div>
</footer>

<div class="action-bar">
  <a class="btn btn--ghost" href="tel:%(tel)s">%(ic_phone)s Call</a>
  <a class="btn btn--whatsapp" href="%(wa)s" rel="noopener">%(wa_icon)s WhatsApp</a>
</div>
</body>
</html>
""" % {
        "inst": e(C.INSTRUCTOR), "founded": C.FOUNDED, "tel": C.PHONE_TEL,
        "phone": e(C.PHONE_DISPLAY), "email": e(C.EMAIL), "svc": svc, "areas": areas,
        "res": res, "ack": e(C.ACKNOWLEDGEMENT), "brand": e(C.BRAND),
        "prev": e(C.LEGAL_PREVIOUS), "hours": e(C.HOURS_TEXT),
        "ic_phone": icon("phone", 16), "ic_mail": icon("mail", 16), "wa_icon": WA_SVG,
        "wa": e(wa_link("Hi Gopi, I found Adelaide Confident Driving Academy online and I'd "
                        "like to ask about driving lessons.")),
    }


def crumbs_html(crumbs):
    items = []
    for i, (name, path) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        if last:
            items.append('<li><span aria-current="page">%s</span></li>' % e(name))
        else:
            items.append('<li><a href="%s">%s</a></li>' % (path, e(name)))
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>%s</ol></div></nav>'
            % "".join(items))


# ---------------------------------------------------------------------------
# Reusable blocks
# ---------------------------------------------------------------------------

def rating_badge(dark=True):
    return ('<a class="rating-badge" href="%s" target="_blank" rel="noopener">'
            '%s<span class="rb-text"><b>%s</b> from %d Google reviews</span>'
            '<span class="rb-chip">Verified</span></a>'
            % (e(C.GOOGLE_PROFILE), STARS, C.RATING, C.REVIEW_COUNT))


def booking_widget():
    routes = [(s["nav"], s["nav"]) for s in C.SERVICES]
    route_opts = "".join(
        '<label class="opt"><input type="radio" name="route" value="%s"%s><span>%s</span></label>'
        % (e(v), ' checked' if i == 0 else '', e(l)) for i, (l, v) in enumerate(routes))
    gear_opts = "".join(
        '<label class="opt"><input type="radio" name="gearbox" value="%s"%s><span>%s</span></label>'
        % (e(v), ' checked' if i == 0 else '', e(v)) for i, v in enumerate(["Automatic", "Manual"]))
    timing = ["Weekday mornings", "Weekday afternoons or evenings", "Weekends",
              "Urgent, within the next two weeks"]
    time_opts = "".join(
        '<label class="opt"><input type="radio" name="timing" value="%s"%s><span>%s</span></label>'
        % (e(v), ' checked' if i == 0 else '', e(v)) for i, v in enumerate(timing))
    chips = "".join('<button type="button">%s</button>' % e(s) for s in C.SUBURB_CHIPS)

    return """<div class="booking" id="book">
  <div class="booking-head">
    <div>
      <h2>Book a lesson in four taps</h2>
      <p>Sends %(inst)s a tidy WhatsApp message with everything he needs.</p>
    </div>
    <span class="booking-step-count" id="booking-step-count">Step 1 of 4</span>
  </div>

  <div class="progress" role="progressbar" aria-label="Booking progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="25">
    <i id="booking-progress"></i>
  </div>

  <form id="booking-form" novalidate>
    <fieldset class="step is-active" data-require="route" data-autoadvance="1"
              data-error="Choose the training path that fits you best.">
      <legend class="step-q">Which licence pathway are you after?</legend>
      <p class="step-hint">Not sure? Pick the closest and %(inst)s will sort it out with you.</p>
      <div class="opt-list">%(routes)s</div>
    </fieldset>

    <fieldset class="step" data-require="gearbox" data-autoadvance="1"
              data-error="Choose automatic or manual.">
      <legend class="step-q">Automatic or manual?</legend>
      <p class="step-hint">An automatic assessment gives you an automatic-only licence condition.</p>
      <div class="opt-list opt-list--2">%(gears)s</div>
    </fieldset>

    <fieldset class="step" data-require="suburb"
              data-error="Enter the suburb you would like to be picked up from.">
      <legend class="step-q">Which suburb are you in?</legend>
      <p class="step-hint">Pickup from home, work or uni is usually fine within the service areas.</p>
      <div class="field">
        <label for="suburb">Suburb or area</label>
        <input type="text" id="suburb" name="suburb" autocomplete="address-level2"
               placeholder="e.g. Mawson Lakes" enterkeyhint="next">
        <div class="suburb-hints">%(chips)s</div>
      </div>
    </fieldset>

    <fieldset class="step" data-require="timing"
              data-error="Let %(inst)s know roughly when suits you.">
      <legend class="step-q">When suits you?</legend>
      <p class="step-hint">Seven days a week, %(hours)s.</p>
      <div class="opt-list">%(times)s</div>
      <div class="booking-summary" id="booking-summary" hidden>
        <dl></dl>
      </div>
    </fieldset>

    <p class="form-error" id="booking-error" role="alert" hidden></p>

    <div class="booking-nav">
      <button type="button" class="btn booking-back" id="booking-back" hidden>Back</button>
      <button type="submit" class="btn btn--primary" id="booking-next">Continue</button>
    </div>

    <p class="booking-fallback" id="booking-result" role="status" hidden></p>
    <p class="booking-fallback">Prefer to talk? Call
      <a href="tel:%(tel)s">%(phone)s</a>.</p>
  </form>
</div>
""" % {"inst": e(C.INSTRUCTOR), "routes": route_opts, "gears": gear_opts,
       "times": time_opts, "chips": chips, "tel": C.PHONE_TEL,
       "phone": e(C.PHONE_DISPLAY), "hours": e(C.HOURS_TEXT.lower())}


def review_cards(limit=None, filters=True):
    items = C.REVIEWS if limit is None else C.REVIEWS[:limit]
    cards = "".join("""<article class="review" data-tags="%(tags)s">
  %(stars)s
  <blockquote>%(text)s</blockquote>
  <footer>
    <span class="avatar" aria-hidden="true">%(ini)s</span>
    <span class="who"><b>%(name)s</b><span>%(tag)s</span></span>
  </footer>
</article>""" % {"tags": e("|".join(r["tags"])), "stars": STARS, "text": e(r["text"]),
                 "ini": e(initials(r["name"])), "name": e(r["name"]), "tag": e(r["tag"])}
                   for r in items)

    bar = ""
    if filters:
        btns = "".join(
            '<button class="filter-btn" type="button" data-filter="%s" aria-pressed="%s">%s</button>'
            % (e(slug), "true" if slug == "all" else "false", e(label))
            for slug, label in C.REVIEW_TAGS)
        bar = ('<div class="filter-bar" id="review-filter" role="group" '
               'aria-label="Filter reviews">%s</div>'
               '<p class="sr-only" id="review-count" role="status"></p>' % btns)

    return bar + '<div class="review-grid" id="review-grid">%s</div>' % cards


def price_table(group_key):
    g = C.PRICING[group_key]
    cards = "".join("""<div class="price-card%(feat)s">
  %(flag)s
  <span class="pc-dur">%(dur)s</span>
  <h3>%(name)s</h3>
  <p class="pc-amt"><small>from</small> $%(price)s</p>
  <p>%(desc)s</p>
  <a class="btn btn--outline btn--sm" href="/#book">Book this</a>
</div>""" % {"feat": " is-featured" if it["featured"] else "",
             "flag": '<span class="pc-flag">Popular</span>' if it["featured"] else "",
             "dur": e(it["dur"]), "name": e(it["name"]), "price": e(it["price"]),
             "desc": e(it["desc"])} for it in g["items"])
    return '<div class="price-grid">%s</div>' % cards


def faq_block(pairs):
    return '<div class="faq">%s</div>' % "".join(
        '<details><summary>%s</summary><div class="faq-body"><p>%s</p></div></details>'
        % (e(q), e(a)) for q, a in pairs)


def cta_band(heading, body):
    return """<section class="section"><div class="wrap">
  <div class="cta-band reveal">
    <h2>%(h)s</h2>
    <p>%(b)s</p>
    <div class="btn-row">
      <a class="btn btn--whatsapp pulse" href="%(wa)s" rel="noopener">%(wa_icon)s Book on WhatsApp</a>
      <a class="btn btn--ghost" href="tel:%(tel)s">%(ic)s Call %(phone)s</a>
    </div>
  </div>
</div></section>""" % {
        "h": e(heading), "b": e(body), "wa_icon": WA_SVG, "ic": icon("phone", 18),
        "tel": C.PHONE_TEL, "phone": e(C.PHONE_DISPLAY),
        "wa": e(wa_link("Hi Gopi, I'd like to book a driving lesson. Here's a bit about "
                        "where I'm at:")),
    }


def instructor_photos():
    hero = C.PHOTOS["hero"]
    if photo_exists(hero["file"]):
        media = '<img src="/assets/img/team/%s" alt="%s" width="800" height="1000" loading="lazy">' \
                % (e(hero["file"]), e(hero["alt"]))
    else:
        media = ('<p class="ph-note"><b>Photo of Gopi goes here</b>'
                 'Drop a portrait at <code>/assets/img/team/%s</code> and rebuild. '
                 'Portrait crop, roughly 800 x 1000.</p>' % e(hero["file"]))
    strip = ""
    for p in C.PHOTOS["strip"]:
        if photo_exists(p["file"]):
            strip += ('<div><img src="/assets/img/team/%s" alt="%s" width="400" height="400" '
                      'loading="lazy"></div>' % (e(p["file"]), e(p["alt"])))
        else:
            strip += '<div>%s</div>' % e(p["file"])
    return """<div>
  <div class="photo-frame">
    %(media)s
    <div class="photo-caption">
      <span>%(cap_label)s</span>
      <b>%(cap_name)s</b>
    </div>
  </div>
  <div class="photo-strip">%(strip)s</div>
</div>""" % {"media": media, "strip": strip,
             "cap_label": e(hero.get("caption_label", "Lead instructor")),
             "cap_name": e(hero.get("caption_name", C.INSTRUCTOR))}


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

def page_home():
    path = "/"
    schema = jsonld(ld_website(), ld_business(), ld_person(),
                    ld_faq(C.FAQS[:6]),
                    ld_breadcrumbs([("Home", "/")]))
    svc_cards = "".join("""<article class="card card--dark card-glow %(glow)s reveal" data-delay="%(d)d" style="--glow-delay:%(gd).1fs">
  <span class="card-icon">%(icon)s</span>
  <span class="%(chipclass)s" style="align-self:flex-start;margin-bottom:12px">%(chip)s</span>
  <h3>%(nav)s</h3>
  <p>%(sum)s</p>
  <a class="card-link" href="/services/%(slug)s/">%(nav)s</a>
</article>""" % {"d": i * 70, "gd": i * 0.6, "glow": glow_class(s),
                 "chipclass": chip_class(s, "chip--gold"),
                 "icon": icon(s["icon"]), "chip": e(s["chip"]),
                 "nav": e(s["nav"]), "sum": e(s["summary"]), "slug": s["slug"],
                 } for i, s in enumerate(C.SERVICES))

    creds = "".join('<li><span class="tick" aria-hidden="true">&#10003;</span>'
                    '<span><b>%s.</b> %s</span></li>' % (e(t), e(d)) for t, d in C.CREDENTIALS)

    areas = "".join("""<div class="area-block reveal">
  <h3>%(name)s</h3>
  <p>%(blurb)s</p>
  <ul class="suburb-list">%(subs)s</ul>
</div>""" % {"name": e(a["name"]), "blurb": e(a["blurb"]),
             "subs": "".join("<li>%s</li>" % e(s) for s in a["suburbs"][:7])}
                    for a in C.AREAS)

    body = """%(pre)s%(head)s
<main id="main">

<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        %(badge)s
        <p class="hero-credential">Highly Accredited CBTA Certified Examiner in Adelaide</p>
        <h1>Drive with certainty. <em>Pass with confidence.</em></h1>
        <p class="lede">One-to-one driving lessons across Adelaide with Gopi, a CBTA Certified
        Examiner teaching South Australians since 2006. CBT&amp;A logbook training, VORT test
        preparation and overseas licence conversion, taught calmly and at the pace you actually
        need.</p>
        <div class="btn-row">
          <a class="btn btn--whatsapp pulse" href="#book">%(wa_icon)s Instant WhatsApp booking</a>
          <a class="btn btn--ghost" href="tel:%(tel)s">%(ic_phone)s Call %(phone)s</a>
        </div>
        <div class="microstats">
          <div><b><span data-count="20" data-suffix="+">20+</span></b><span>Years instructing</span></div>
          <div><b><span data-count="5.0">5.0</span></b><span>Google rating</span></div>
          <div><b><span data-count="72" data-suffix="+">72+</span></b><span>Five star reviews</span></div>
          <div><b>1:1</b><span>Every single lesson</span></div>
        </div>
      </div>
      <div class="reveal" data-delay="120">%(booking)s</div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">%(ic_star)s What we teach</p>
      <h2>Five ways to get licensed, and one instructor for all of them</h2>
      <p class="lede">Every learner arrives from somewhere different. A nervous seventeen year
      old, a driver with twenty years of experience overseas, someone who has failed a VORT
      twice. The pathway changes. The one-to-one approach does not.</p>
    </div>
    <div class="grid grid--3">%(services)s</div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="instructor">
      %(photos)s
      <div>
        <p class="eyebrow">Meet your instructor</p>
        <h2>Gopi has been teaching Adelaide to drive since 2006</h2>
        <p class="lede">Read the reviews and one word keeps coming back: patient. Twenty years
        in, with a background in automobile engineering, Gopi has seen every mistake a learner
        can make. None of them are worth raising a voice over.</p>
        <ul class="cred-list">%(creds)s</ul>
        <div class="btn-row mt-32">
          <a class="btn btn--primary" href="/about/">More about Gopi</a>
          <a class="btn btn--outline" href="/reviews/">Read all 72 reviews</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow">%(ic_star)s Wall of confidence</p>
      <h2>Five stars, seventy-two times over</h2>
      <p class="lede" style="margin-inline:auto">Every review below is a real, verified Google
      review. Filter by what matters to your situation.</p>
    </div>
    %(reviews)s
    <div class="center mt-32">
      <a class="btn btn--outline" href="%(gprofile)s" target="_blank" rel="noopener">See them on Google</a>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">%(ic_pin)s Where we teach</p>
      <h2>Driving lessons across Adelaide</h2>
      <p class="lede">Pickup from home, work or uni is usually fine anywhere in the service
      areas. Not sure whether your suburb is covered? Send a message and ask.</p>
    </div>
    <div class="grid grid--2">%(areas)s</div>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="section-head section-head--center">
      <p class="eyebrow">Common questions</p>
      <h2>Everything people ask before booking</h2>
    </div>
    %(faq)s
    <div class="center mt-32"><a class="btn btn--outline" href="/faq/">See all questions</a></div>
  </div>
</section>

%(cta)s
</main>
%(foot)s""" % {
        "pre": preloader(), "head": header(path), "badge": rating_badge(),
        "wa_icon": WA_SVG, "ic_phone": icon("phone", 18), "ic_star": icon("star", 14),
        "ic_pin": icon("pin", 14), "tel": C.PHONE_TEL, "phone": e(C.PHONE_DISPLAY),
        "booking": booking_widget(), "services": svc_cards, "photos": instructor_photos(),
        "creds": creds, "reviews": review_cards(limit=6),
        "gprofile": e(C.GOOGLE_PROFILE), "areas": areas,
        "faq": faq_block(C.FAQS[:6]),
        "cta": cta_band("Ready when you are",
                        "Four taps and Gopi has your pathway, transmission, suburb and "
                        "preferred timing. Most enquiries get a reply the same day."),
        "foot": footer(),
    }

    return head({
        "path": path,
        "title": "Highly Accredited CBTA Certified Examiner in Adelaide",
        "meta": "CBTA Certified Examiner Gopi teaches one-to-one driving lessons across Adelaide. CBT&A, VORT prep and licence conversion. 5.0 stars, 72 reviews.",
        "schema": schema,
    }) + body


def page_service(svc):
    path = "/services/%s/" % svc["slug"]
    crumbs = [("Home", "/"), ("Lessons", "/services/"), (svc["nav"], path)]
    schema = jsonld(ld_business(), ld_service(svc), ld_faq(svc["faqs"]),
                    ld_breadcrumbs(crumbs))

    intro = "".join("<p>%s</p>" % e(p) for p in svc["intro"])
    benefits = "".join("""<article class="card reveal" data-delay="%d">
  <h3>%s</h3><p>%s</p>
</article>""" % (i * 60, e(t), e(d)) for i, (t, d) in enumerate(svc["benefits"]))
    steps = "".join("<li><div><h3>%s</h3><p>%s</p></div></li>" % (e(t), e(d))
                    for t, d in svc["process"])

    others = "".join('<article class="card reveal"><span class="card-icon">%s</span>'
                     '<h3>%s</h3><p>%s</p>'
                     '<a class="card-link" href="/services/%s/">Read more</a></article>'
                     % (icon(o["icon"]), e(o["nav"]), e(o["summary"]), o["slug"])
                     for o in C.SERVICES if o["slug"] != svc["slug"])

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <span class="%(chipclass)s">%(chip)s</span>
    <h1 style="margin-top:14px">%(h1)s</h1>
    <p class="lede">%(tag)s</p>
    <div class="btn-row mt-24">
      <a class="btn btn--whatsapp pulse" href="%(wa)s" rel="noopener">%(wa_icon)s Book %(nav)s</a>
      <a class="btn btn--ghost" href="tel:%(tel)s">%(ic)s Call %(phone)s</a>
    </div>
  </div>
</section>
%(marquee)s
<section class="section">
  <div class="wrap wrap--narrow prose">%(intro)s</div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Why this pathway</p>
      <h2>What you get</h2>
    </div>
    <div class="grid grid--2">%(benefits)s</div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap wrap--narrow">
    <div class="section-head">
      <p class="eyebrow">How it runs</p>
      <h2>From first lesson to licence</h2>
    </div>
    <ol class="steps">%(steps)s</ol>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">Pricing</p>
      <h2>%(plabel)s</h2>
      <p class="lede">%(pnote)s</p>
    </div>
    %(prices)s
    <p class="price-note">%(disclaimer)s</p>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap wrap--narrow">
    <div class="section-head"><p class="eyebrow">Questions</p><h2>About %(nav)s</h2></div>
    %(faq)s
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Other pathways</p><h2>Not quite right for you?</h2></div>
    <div class="grid grid--3">%(others)s</div>
  </div>
</section>

%(cta)s
</main>
%(foot)s""" % {
        "head": header("/services/"), "crumbs": crumbs_html(crumbs), "chip": e(svc["chip"]),
        "chipclass": chip_class(svc, "chip--dark"), "marquee": marquee_band(svc),
        "h1": e(svc["h1"]), "tag": e(svc["tagline"]), "wa_icon": WA_SVG,
        "ic": icon("phone", 18), "tel": C.PHONE_TEL, "phone": e(C.PHONE_DISPLAY),
        "nav": e(svc["nav"]), "intro": intro, "benefits": benefits, "steps": steps,
        "plabel": e(C.PRICING[svc["price_group"]]["label"]),
        "pnote": e(C.PRICING[svc["price_group"]]["note"]),
        "prices": price_table(svc["price_group"]), "disclaimer": e(C.PRICE_DISCLAIMER),
        "faq": faq_block(svc["faqs"]), "others": others,
        "wa": e(wa_link("Hi Gopi, I'm interested in %s with Adelaide Confident Driving "
                        "Academy. Could you tell me about availability?" % svc["nav"].lower())),
        "cta": cta_band("Start with one lesson",
                        "You do not have to commit to a package to find out where you stand. "
                        "Book a single lesson and take it from there."),
        "foot": footer(),
    }

    return head({"path": path, "title": svc["title"], "meta": svc["meta"],
                 "og_type": "article", "schema": schema}) + body


def page_services_index():
    path = "/services/"
    crumbs = [("Home", "/"), ("Lessons", path)]
    schema = jsonld(ld_business(), ld_breadcrumbs(crumbs), {
        "@type": "ItemList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": s["nav"],
                             "url": url("/services/%s/" % s["slug"])}
                            for i, s in enumerate(C.SERVICES)],
    })
    cards = "".join("""<article class="card reveal" data-delay="%(d)d">
  <span class="card-icon">%(icon)s</span>
  <span class="%(chipclass)s" style="align-self:flex-start;margin-bottom:12px">%(chip)s</span>
  <h3>%(nav)s</h3><p>%(sum)s</p>
  <a class="card-link" href="/services/%(slug)s/">%(nav)s</a>
</article>""" % {"d": i * 60, "chipclass": chip_class(s, "chip--gold"),
                 "icon": icon(s["icon"]), "chip": e(s["chip"]),
                 "nav": e(s["nav"]), "sum": e(s["summary"]), "slug": s["slug"]}
                    for i, s in enumerate(C.SERVICES))

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Driving lessons in Adelaide</h1>
    <p class="lede">Five pathways, one instructor. Whether you are starting from zero,
    preparing for a VORT, or converting an overseas licence, the training is one to one and
    built around where you actually are.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Choose a pathway</p>
    <h2>Five ways to get your South Australian licence</h2></div>
    <div class="grid grid--3">%(cards)s</div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head section-head--center">
      <p class="eyebrow">Which one?</p>
      <h2>CBT&amp;A or VORT, in one paragraph</h2>
    </div>
    <div class="wrap--narrow prose" style="margin-inline:auto">
      <p>CBT&amp;A is the logbook method. You work through 30 competency tasks and each one is
      signed off as you demonstrate it, so no single day decides the outcome. The VORT is one
      assessed drive after 75 logged supervised hours, where you need 90 percent or better and
      no road law breaches at all.</p>
      <p>If test pressure is your enemy, take CBT&amp;A. If you are a confident driver who would
      rather get it done in one sitting, the VORT is faster. Most people who are unsure should
      book a single lesson and decide afterwards, which is a far better basis than guessing.</p>
    </div>
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs), "cards": cards,
               "cta": cta_band("Not sure which pathway fits?",
                               "Send a message describing where you are up to and Gopi will "
                               "tell you honestly which route makes more sense."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Driving Lessons Adelaide | CBT&A, VORT & Conversion",
        "meta": "Compare driving lesson pathways in Adelaide: CBT&A logbook training, VORT prep, overseas conversion, beginner and refresher lessons.",
        "schema": schema}) + body


def page_about():
    path = "/about/"
    crumbs = [("Home", "/"), ("About Gopi", path)]
    schema = jsonld(ld_business(), ld_person(), ld_breadcrumbs(crumbs))
    bio = "".join("<p>%s</p>" % e(p) for p in C.INSTRUCTOR_BIO)
    creds = "".join('<li><span class="tick" aria-hidden="true">&#10003;</span>'
                    '<span><b>%s.</b> %s</span></li>' % (e(t), e(d)) for t, d in C.CREDENTIALS)

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Meet Gopi</h1>
    <p class="lede">Lead instructor, CBTA Certified Examiner, and the reason seventy-two people
    left five star reviews.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="instructor">
      %(photos)s
      <div class="prose">
        %(bio)s
        <h2 style="margin-top:1.6em">Credentials</h2>
        <ul class="cred-list" style="list-style:none;padding:0">%(creds)s</ul>
        <div class="btn-row mt-32">
          <a class="btn btn--whatsapp pulse" href="%(wa)s" rel="noopener">%(wa_icon)s Message Gopi</a>
          <a class="btn btn--outline" href="/reviews/">Read the reviews</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--dark">
  <div class="wrap wrap--narrow">
    <div class="section-head"><p class="eyebrow">The approach</p><h2>How lessons actually run</h2></div>
    <ol class="steps">
      <li><div><h3>You are assessed, not assumed</h3><p>The first lesson works out where you
      genuinely are. Nobody sits through material they do not need, and nobody gets pushed past
      something they have not got yet.</p></div></li>
      <li><div><h3>Explained before attempted</h3><p>Every manoeuvre gets talked through before
      you are asked to perform it. Reviewers mention this more than anything else, which
      suggests other instructors do not always bother.</p></div></li>
      <li><div><h3>The same instructor, every time</h3><p>No rotating roster. Half of learning
      to drive is trusting the voice in the passenger seat, and that takes continuity.</p></div></li>
      <li><div><h3>Honest about readiness</h3><p>If you are not ready to book a test, you will
      be told. That is worth more than an instructor who takes the booking fee and lets you
      find out the hard way.</p></div></li>
    </ol>
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs),
               "photos": instructor_photos(), "bio": bio, "creds": creds, "wa_icon": WA_SVG,
               "wa": e(wa_link("Hi Gopi, I read your about page and I'd like to ask about "
                               "driving lessons.")),
               "cta": cta_band("Twenty years of experience, one lesson at a time",
                               "Book a single lesson and see how it goes. No packages, no "
                               "pressure, no commitment beyond the first hour and a half."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "About Gopi | Adelaide Driving Instructor Since 2006",
        "meta": "Gopi has taught South Australians to drive since 2006. Patient, one-to-one instruction across Adelaide. 5.0 stars from 72 Google reviews.",
        "og_type": "profile", "schema": schema}) + body


def page_reviews():
    path = "/reviews/"
    crumbs = [("Home", "/"), ("Reviews", path)]
    schema = jsonld(ld_business(), ld_breadcrumbs(crumbs))

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    %(badge)s
    <h1>Seventy-two reviews. Not one below five stars.</h1>
    <p class="lede">These are verbatim Google reviews from real students. Filter by what
    matches your situation, or read them on Google yourself.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    %(reviews)s
    <div class="center mt-40">
      <a class="btn btn--primary" href="%(g)s" target="_blank" rel="noopener">Read them on Google</a>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap wrap--narrow prose">
    <h2>What keeps coming up</h2>
    <p><strong>Patience.</strong> It is in more reviews than any other word. One student
    completed her lessons in the ninth month of pregnancy and credits the calm approach for
    making it possible. Another had been through several instructors before finding one who
    explained things properly.</p>
    <p><strong>First attempt passes.</strong> Several reviewers mention passing on the first
    try, including one who passed CBT&amp;A with an auditor sitting in the car. Another
    completed the full licence test after just two training sessions.</p>
    <p><strong>Clear explanation.</strong> Breaking a task down and making sure it is understood
    before it is attempted on the road. It sounds obvious. It is apparently not universal.</p>
    <p>If you have had lessons with Gopi, a review helps other learners more than you would
    think. It is the main way people find a driving instructor now.</p>
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs), "badge": rating_badge(),
               "reviews": review_cards(), "g": e(C.GOOGLE_PROFILE),
               "cta": cta_band("Join them",
                               "Book a lesson and find out why seventy-two people bothered to "
                               "write a review."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Reviews | 5.0 Stars from 72 Adelaide Students",
        "meta": "Verified Google reviews for Adelaide Confident Driving Academy. 5.0 stars from 72 students across CBT&A, VORT prep and first attempt passes.",
        "schema": schema}) + body


def page_pricing():
    path = "/pricing/"
    crumbs = [("Home", "/"), ("Pricing", path)]
    price_faqs = [
        ("How much do driving lessons cost in Adelaide?",
         "Across Adelaide, individual lessons typically fall between $70 and $90 per hour. "
         "Our CBT&A lessons start from $180 for 90 minutes, which works out at $120 per hour, "
         "reflecting one-to-one instruction from an Authorised Examiner who can sign off your "
         "competency tasks directly rather than sending you elsewhere for assessment."),
        ("Is the package cheaper than booking single lessons?",
         "Yes. The 10 lesson CBT&A package works out lower per lesson than booking ten singles, "
         "and the VORT packs do the same. That said, do not buy a package until you have had at "
         "least one lesson and know roughly how many you need."),
        ("What payment methods do you accept?",
         "Talk to Gopi when you book. Payment is arranged directly and there is nothing to pay "
         "on this website."),
        ("Are the prices fixed?",
         "They are indicative starting points. Where you are located, how long the lesson runs "
         "and how many sessions you book all affect the final figure. You will get a firm number "
         "before anything is confirmed."),
        ("Do I pay for the VORT test itself separately?",
         "The listed VORT test price covers the assessment conducted by an examiner in the "
         "instructor's dual-control vehicle, including an hour of practice beforehand. "
         "Government fees for your licence are separate and paid to Service SA."),
    ]
    schema = jsonld(ld_business(), ld_faq(price_faqs), ld_breadcrumbs(crumbs))

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Driving lesson prices in Adelaide</h1>
    <p class="lede">Published openly rather than hidden behind an enquiry form. These are
    starting points, and you will get a firm quote before anything is booked.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head pricing-group pricing-group--yellow">
      <p class="eyebrow">%(l1)s</p>
      <h2>Logbook lessons and sign-offs</h2>
      <p class="lede">%(n1)s</p>
    </div>
    %(p1)s
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    <div class="section-head pricing-group pricing-group--red">
      <p class="eyebrow">%(l2)s</p>
      <h2>Test preparation and test day</h2>
      <p class="lede">%(n2)s</p>
    </div>
    %(p2)s
    <p class="price-note">%(disclaimer)s</p>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">
    <div class="section-head"><p class="eyebrow">Pricing questions</p><h2>The honest answers</h2></div>
    %(faq)s
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs),
               "l1": e(C.PRICING["cbta"]["label"]), "n1": e(C.PRICING["cbta"]["note"]),
               "p1": price_table("cbta"),
               "l2": e(C.PRICING["vort"]["label"]), "n2": e(C.PRICING["vort"]["note"]),
               "p2": price_table("vort"), "disclaimer": e(C.PRICE_DISCLAIMER),
               "faq": faq_block(price_faqs),
               "cta": cta_band("Get a firm quote",
                               "Tell Gopi your suburb, your pathway and roughly where you are "
                               "up to, and you will get a real number rather than a range."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Driving Lesson Prices Adelaide | CBT&A & VORT Costs",
        "meta": "Driving lesson prices in Adelaide. CBT&A from $180 for 90 minutes, a 10 lesson package from $1700, and VORT prep from $120. Published openly.",
        "schema": schema}) + body


def page_areas():
    path = "/service-areas/"
    crumbs = [("Home", "/"), ("Service areas", path)]
    schema = jsonld(ld_business(), ld_breadcrumbs(crumbs))
    blocks = "".join("""<div class="area-block reveal" id="%(slug)s">
  <h3>%(name)s</h3>
  <p>%(blurb)s</p>
  <ul class="suburb-list">%(subs)s</ul>
  <div class="btn-row mt-24">
    <a class="btn btn--outline btn--sm" href="/#book">Book in %(short)s</a>
  </div>
</div>""" % {"slug": a["slug"], "name": e(a["name"]), "blurb": e(a["blurb"]),
             "subs": "".join("<li>%s</li>" % e(s) for s in a["suburbs"]),
             "short": e(a["name"].split(" and ")[0].lower())} for a in C.AREAS)

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Driving lessons across Adelaide</h1>
    <p class="lede">Pickup from home, work or uni is usually fine within the service areas.
    Lessons are taught on the roads you will actually be tested on, not on a generic circuit.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><p class="eyebrow">Coverage</p>
    <h2>Suburbs across five regions of Adelaide</h2></div>
    <div class="grid grid--2">%(blocks)s</div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap wrap--narrow prose">
    <h2>Why the suburb matters more than people think</h2>
    <p>Adelaide does not drive the same way everywhere. The inner grid is one-way streets, tram
    lines and constant lane discipline. The north is wide arterials and long merges at higher
    speeds. The west has heavy freight on Port Road and a lot of unmarked intersections through
    the older street layouts. The east means gradients, hill starts and roundabout geometry that
    catches people out. The south, down to Marion, means Anzac Highway and Marion Road traffic,
    the Glenelg tram line, and more roundabouts than anywhere else on the list.</p>
    <p>Learning in the area you will be assessed in is not a small advantage. It is most of the
    reason people fail on roads they have never seen before.</p>
    <p>If your suburb is not listed above, ask anyway. The lists are the common ones, not the
    complete ones.</p>
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs), "blocks": blocks,
               "cta": cta_band("Is your suburb covered?",
                               "Send a message with where you are and you will get a straight "
                               "yes or no, not a runaround."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Driving Lessons Near Me | Adelaide Suburbs Covered",
        "meta": "Driving lessons across Adelaide CBD, northern, western, eastern and southern suburbs, from Salisbury to Marion. Pickup from home, work or uni.",
        "schema": schema}) + body


def page_faq():
    path = "/faq/"
    crumbs = [("Home", "/"), ("FAQ", path)]
    all_faqs = list(C.FAQS)
    for s in C.SERVICES:
        all_faqs.extend(s["faqs"])
    webpage = {
        "@type": "WebPage",
        "@id": url(path),
        "url": url(path),
        "name": "Frequently asked questions",
        "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".faq-body"]},
    }
    schema = jsonld(ld_business(), ld_faq(all_faqs), ld_breadcrumbs(crumbs), webpage)

    sections = '<div class="section-head"><h2>General</h2></div>' + faq_block(C.FAQS)
    for s in C.SERVICES:
        sections += ('<div class="section-head mt-40"><h2>%s</h2>'
                     '<p class="lede"><a href="/services/%s/">Full details on the %s page</a></p></div>%s'
                     % (e(s["nav"]), s["slug"], e(s["nav"].lower()), faq_block(s["faqs"])))

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Frequently asked questions</h1>
    <p class="lede">Everything people ask before booking a first lesson, answered properly.</p>
  </div>
</section>

<section class="section">
  <div class="wrap wrap--narrow">%(sections)s</div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs), "sections": sections,
               "cta": cta_band("Still got a question?",
                               "Ask it directly. Gopi answers messages himself and usually the "
                               "same day."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Driving Lesson FAQ Adelaide | CBT&A vs VORT Answered",
        "meta": "Common questions about driving lessons in Adelaide: CBT&A versus VORT, automatic or manual, how many lessons you need, and what it costs.",
        "schema": schema}) + body


def page_contact():
    path = "/contact/"
    crumbs = [("Home", "/"), ("Contact", path)]
    schema = jsonld(ld_business(), ld_breadcrumbs(crumbs), {
        "@type": "ContactPage", "@id": url(path), "url": url(path),
        "about": {"@id": url("/#business")},
    })

    body = """%(head)s
<main id="main">
<section class="page-hero">
  %(crumbs)s
  <div class="wrap">
    <h1>Book a driving lesson</h1>
    <p class="lede">The booking form below sends Gopi one tidy WhatsApp message with your
    pathway, transmission, suburb and preferred timing. Calling works just as well.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="hero-grid" style="align-items:start">
      <div>
        <div class="section-head"><p class="eyebrow">Get in touch</p><h2>Three ways to reach Gopi</h2></div>
        <div class="grid" style="gap:16px">
          <article class="card">
            <span class="card-icon">%(ic_wa)s</span>
            <h3>WhatsApp</h3>
            <p>Fastest option, and the one most people use. Messages usually get a reply the
            same day.</p>
            <a class="btn btn--whatsapp mt-24" href="%(wa)s" rel="noopener">%(wa_icon)s Open WhatsApp</a>
          </article>
          <article class="card">
            <span class="card-icon">%(ic_phone)s</span>
            <h3>Phone or SMS</h3>
            <p>Call or text %(phone)s. If Gopi is mid-lesson he will call back.</p>
            <a class="btn btn--outline mt-24" href="tel:%(tel)s">Call %(phone)s</a>
          </article>
          <article class="card">
            <span class="card-icon">%(ic_mail)s</span>
            <h3>Email</h3>
            <p>Better for longer questions or anything with paperwork attached.</p>
            <a class="btn btn--outline mt-24" href="mailto:%(email)s">%(email)s</a>
          </article>
        </div>
        <div class="card mt-24">
          <span class="card-icon">%(ic_clock)s</span>
          <h3>Hours and coverage</h3>
          <p><strong>%(hours)s.</strong> Early morning and evening slots are often available,
          which helps if you are working or studying full time.</p>
          <p class="mt-24">Serving Adelaide CBD and inner suburbs, northern suburbs, western
          suburbs, eastern suburbs and southern suburbs down to Marion.</p>
        </div>
      </div>
      <div>%(booking)s</div>
    </div>
  </div>
</section>
%(cta)s
</main>
%(foot)s""" % {"head": header(path), "crumbs": crumbs_html(crumbs),
               "ic_wa": WA_SVG, "ic_phone": icon("phone"), "ic_mail": icon("mail"),
               "ic_clock": icon("clock"), "wa_icon": WA_SVG,
               "wa": e(wa_link("Hi Gopi, I'd like to book a driving lesson with Adelaide "
                               "Confident Driving Academy.")),
               "phone": e(C.PHONE_DISPLAY), "tel": C.PHONE_TEL, "email": e(C.EMAIL),
               "hours": e(C.HOURS_TEXT), "booking": booking_widget(),
               "cta": cta_band("One lesson is all it takes to know",
                               "You will get an honest read on where you stand and a realistic "
                               "estimate of what is left to do."),
               "foot": footer()}

    return head({
        "path": path,
        "title": "Contact | Book a Driving Lesson in Adelaide",
        "meta": "Book driving lessons in Adelaide with Gopi. WhatsApp, call or text 0423 457 296, seven days a week until 8pm. Five suburb regions covered.",
        "schema": schema}) + body


def page_404():
    body = """%(head)s
<main id="main">
<section class="page-hero">
  <div class="wrap">
    <h1>That page has moved</h1>
    <p class="lede">This site used to be Adelaide Driver Training Academy SA, so a few old
    links point at pages that no longer exist. Everything is still here, just under a new
    name.</p>
    <div class="btn-row mt-24">
      <a class="btn btn--primary" href="/">Go to the home page</a>
      <a class="btn btn--ghost" href="/services/">Browse lessons</a>
    </div>
  </div>
</section>
<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Popular pages</h2></div>
    <div class="grid grid--3">
      <article class="card"><h3>CBT&amp;A logbook training</h3><p>The logbook method, with no
      pass or fail final test.</p><a class="card-link" href="/services/cbta-logbook-training/">Read more</a></article>
      <article class="card"><h3>VORT test preparation</h3><p>Mock tests and test day bookings.</p>
      <a class="card-link" href="/services/vort-test-preparation/">Read more</a></article>
      <article class="card"><h3>Pricing</h3><p>What lessons and tests actually cost.</p>
      <a class="card-link" href="/pricing/">Read more</a></article>
    </div>
  </div>
</section>
</main>
%(foot)s""" % {"head": header(""), "foot": footer()}

    return head({"path": "/404.html", "title": "Page not found | Adelaide Confident Driving",
                 "meta": "That page could not be found. Browse driving lessons, pricing and contact details for Adelaide Confident Driving Academy.",
                 "noindex": True}) + body


# ---------------------------------------------------------------------------
# Non-HTML output
# ---------------------------------------------------------------------------

def all_paths():
    paths = [("/", "1.0", "weekly"), ("/services/", "0.9", "monthly")]
    paths += [("/services/%s/" % s["slug"], "0.9", "monthly") for s in C.SERVICES]
    paths += [("/pricing/", "0.8", "monthly"), ("/about/", "0.8", "monthly"),
              ("/reviews/", "0.8", "weekly"), ("/service-areas/", "0.7", "monthly"),
              ("/faq/", "0.7", "monthly"), ("/contact/", "0.9", "monthly")]
    return paths


def sitemap():
    entries = "".join(
        "  <url><loc>%s</loc><lastmod>%s</lastmod>"
        "<changefreq>%s</changefreq><priority>%s</priority></url>\n"
        % (url(p), TODAY, freq, pri) for p, pri, freq in all_paths())
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s</urlset>\n'
            % entries)


def robots():
    return """# robots.txt for %(brand)s
# Everything here is public. Crawl it.

User-agent: *
Allow: /
Disallow: /404.html

# Search engines
User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: DuckDuckBot
Allow: /

# AI assistants and answer engines. These send real enquiries now, so they
# are welcome. See /llms.txt for a structured summary of the site.
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: anthropic-ai
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Perplexity-User
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bytespider
Allow: /
User-agent: CCBot
Allow: /
User-agent: meta-externalagent
Allow: /
User-agent: cohere-ai
Allow: /

Sitemap: %(site)s/sitemap.xml
""" % {"brand": C.BRAND, "site": C.SITE_URL}


def llms_txt():
    svc = "\n".join("- [%s](%s): %s" % (s["nav"], url("/services/%s/" % s["slug"]), s["summary"])
                    for s in C.SERVICES)
    areas_line = ", ".join(a["name"] for a in C.AREAS)
    cbta_lines = "\n".join("- %s from $%s" % (it["name"], it["price"])
                           for it in C.PRICING["cbta"]["items"])
    vort_lines = "\n".join("- %s from $%s" % (it["name"], it["price"])
                           for it in C.PRICING["vort"]["items"])
    return """# %(brand)s

> A one-to-one driving school in Adelaide, South Australia, run by %(inst)s, a highly
> accredited CBTA Certified Examiner who has been teaching people to drive since %(founded)s. Rated %(rating)s stars from %(count)d Google
> reviews. Formerly trading as %(prev)s.

## Key facts

- Business: %(brand)s (previously %(prev)s)
- Instructor: %(inst)s, CBTA Certified Examiner, teaching since %(founded)s, background in automobile engineering
- Phone and SMS: %(phone)s
- WhatsApp: https://wa.me/%(wa)s
- Email: %(email)s
- Hours: %(hours)s
- Rating: %(rating)s from %(count)d Google reviews
- Location: Adelaide, South Australia. Service area business, no shopfront.
- Areas served: %(areas_line)s, from Salisbury in the north to Marion in the south.
- Transmissions taught: automatic and manual
- Booking: WhatsApp is the fastest route. There is no online payment or calendar system.

## Services

%(svc)s

## Pricing (indicative, AUD, as at September 2026)

CBT&A logbook training:
%(cbta_lines)s

VORT test preparation:
%(vort_lines)s

The VORT is conducted only in the instructor's dual-control vehicle. There is no option to
sit the VORT in a student's personal vehicle: the instructor's car has dual brake controls
that a student's car does not, which removes the risk of a roadworthiness or tyre issue on
test day. The instructor-vehicle price includes an hour of practice in it beforehand.

## Pages

- [Home](%(site)s/): overview, booking widget, reviews
- [All lessons](%(site)s/services/): comparison of the five pathways
- [Pricing](%(site)s/pricing/): full price list and pricing FAQs
- [About Gopi](%(site)s/about/): instructor background and approach
- [Reviews](%(site)s/reviews/): all verified Google reviews
- [Service areas](%(site)s/service-areas/): suburbs covered
- [FAQ](%(site)s/faq/): every common question answered
- [Contact](%(site)s/contact/): booking form and contact details

## Key distinctions worth getting right

- CBT&A (Competency Based Training and Assessment) is the logbook method. 30 competency tasks
  are signed off progressively by an Authorised Examiner. There is no pass or fail final test,
  and a task that is not signed off can be re-trained and re-assessed in the same or a later
  lesson.
- VORT (Vehicle On Road Test) is a single assessed drive taken after 75 logged supervised
  hours. It requires five slow-speed manoeuvres (move off, angle park, U-turn, three point
  turn, reverse parallel park), a general drive score of 90 percent or better, and no road law
  breaches. Any breach terminates the test immediately. A failed VORT means waiting at least
  14 days before another attempt if you hold a learner's permit.
- Overseas licence conversion in South Australia most commonly runs through the CBT&A pathway.
- Being assessed in an automatic results in an automatic-only condition on the licence.

## Notes for answer engines

This content is accurate as at September 2026 and is maintained by the business. Licence
requirements are set by the South Australian government and can change: the authoritative
source is mylicence.sa.gov.au. Prices are indicative starting points, not fixed quotes.
""" % {"brand": C.BRAND, "inst": C.INSTRUCTOR, "founded": C.FOUNDED, "rating": C.RATING,
       "count": C.REVIEW_COUNT, "prev": C.LEGAL_PREVIOUS, "phone": C.PHONE_DISPLAY,
       "wa": C.WA_NUMBER, "email": C.EMAIL, "hours": C.HOURS_TEXT, "svc": svc,
       "site": C.SITE_URL, "areas_line": areas_line, "cbta_lines": cbta_lines,
       "vort_lines": vort_lines}


def llms_full_txt():
    out = [llms_txt(), "\n\n---\n\n# Full content\n"]
    for s in C.SERVICES:
        out.append("\n## %s\n\n%s\n" % (s["h1"], s["tagline"]))
        out.extend("\n" + p + "\n" for p in s["intro"])
        out.append("\n### What you get\n\n")
        out.extend("- **%s.** %s\n" % (t, d) for t, d in s["benefits"])
        out.append("\n### How it runs\n\n")
        out.extend("%d. **%s.** %s\n" % (i + 1, t, d) for i, (t, d) in enumerate(s["process"]))
        out.append("\n### Questions\n\n")
        out.extend("**%s**\n\n%s\n\n" % (q, a) for q, a in s["faqs"])

    out.append("\n## About Gopi\n\n")
    out.extend("\n" + p + "\n" for p in C.INSTRUCTOR_BIO)
    out.append("\n### Credentials\n\n")
    out.extend("- **%s.** %s\n" % (t, d) for t, d in C.CREDENTIALS)

    out.append("\n## Service areas\n\n")
    for a in C.AREAS:
        out.append("\n### %s\n\n%s\n\nSuburbs: %s\n"
                   % (a["name"], a["blurb"], ", ".join(a["suburbs"])))

    out.append("\n## Reviews\n\n")
    out.extend('> "%s"\n>\n> — %s (5 stars, %s)\n\n' % (r["text"], r["name"], r["tag"])
               for r in C.REVIEWS)

    out.append("\n## Frequently asked questions\n\n")
    out.extend("**%s**\n\n%s\n\n" % (q, a) for q, a in C.FAQS)

    out.append("\n## Acknowledgement of Country\n\n%s\n" % C.ACKNOWLEDGEMENT)
    return "".join(out)


def manifest():
    return json.dumps({
        "name": C.BRAND,
        "short_name": "ACDA",
        "description": "One-to-one driving lessons across Adelaide with Gopi.",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0B132B",
        "theme_color": "#0B132B",
        "icons": [
            {"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"},
            {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any maskable"},
        ],
    }, indent=2)


# Old site URL -> new site URL. Used for vercel.json and for the Cloudflare
# _redirects file, so the 301s stay in one place.
REDIRECT_MAP = [
    ("/cbta-training-and-assessment", "/services/cbta-logbook-training/"),
    ("/cbta-training-and-assessment/", "/services/cbta-logbook-training/"),
    ("/vort-exam-training", "/services/vort-test-preparation/"),
    ("/vort-exam-training/", "/services/vort-test-preparation/"),
    ("/about-us", "/about/"),
    ("/about-us/", "/about/"),
    ("/contact-us", "/contact/"),
    ("/contact-us/", "/contact/"),
    ("/services", "/services/"),
    ("/book", "/contact/"),
    ("/booking", "/contact/"),
    ("/prices", "/pricing/"),
    ("/testimonials", "/reviews/"),
]


def vercel_json():
    return json.dumps({
        "$schema": "https://openapi.vercel.sh/vercel.json",
        "cleanUrls": True,
        "trailingSlash": True,
        "redirects": [{"source": s, "destination": d, "permanent": True}
                      for s, d in REDIRECT_MAP],
        "headers": [
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "Permissions-Policy",
                 "value": "geolocation=(), microphone=(), camera=(), interest-cohort=()"},
                {"key": "Strict-Transport-Security",
                 "value": "max-age=63072000; includeSubDomains; preload"},
                {"key": "Content-Security-Policy",
                 "value": ("default-src 'self'; "
                           "script-src 'self'; "
                           "style-src 'self' https://fonts.googleapis.com 'unsafe-inline'; "
                           "font-src 'self' https://fonts.gstatic.com; "
                           "img-src 'self' data:; "
                           "connect-src 'self'; "
                           "form-action 'self' https://wa.me; "
                           "frame-ancestors 'self'; "
                           "base-uri 'self'; "
                           "object-src 'none'")},
            ]},
            {"source": "/assets/(.*)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*).html", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=0, must-revalidate"}]},
            {"source": "/llms.txt", "headers": [
                {"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
            {"source": "/llms-full.txt", "headers": [
                {"key": "Content-Type", "value": "text/plain; charset=utf-8"}]},
        ],
    }, indent=2)


def cf_headers():
    return """/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload

/assets/*
  Cache-Control: public, max-age=31536000, immutable

/llms.txt
  Content-Type: text/plain; charset=utf-8

/llms-full.txt
  Content-Type: text/plain; charset=utf-8
"""


def cf_redirects():
    lines = ["# Old Adelaide Driver Training Academy SA paths -> new structure",
             "# Same map as vercel.json. Keep them in sync via build.py.", ""]
    lines += ["%-42s %-44s 301" % (s, d) for s, d in REDIRECT_MAP]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Writer
# ---------------------------------------------------------------------------

def write(rel, text):
    dest = os.path.join(ROOT, rel.lstrip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(text)
    return rel


def main():
    written = []

    written.append(write("index.html", page_home()))
    written.append(write("services/index.html", page_services_index()))
    for s in C.SERVICES:
        written.append(write("services/%s/index.html" % s["slug"], page_service(s)))
    written.append(write("about/index.html", page_about()))
    written.append(write("reviews/index.html", page_reviews()))
    written.append(write("pricing/index.html", page_pricing()))
    written.append(write("service-areas/index.html", page_areas()))
    written.append(write("faq/index.html", page_faq()))
    written.append(write("contact/index.html", page_contact()))
    written.append(write("404.html", page_404()))

    written.append(write("sitemap.xml", sitemap()))
    written.append(write("robots.txt", robots()))
    written.append(write("llms.txt", llms_txt()))
    written.append(write("llms-full.txt", llms_full_txt()))
    written.append(write("site.webmanifest", manifest()))
    written.append(write("vercel.json", vercel_json()))
    written.append(write("_headers", cf_headers()))
    written.append(write("_redirects", cf_redirects()))

    os.makedirs(os.path.join(ROOT, "assets", "img", "team"), exist_ok=True)

    print("Built %d files:" % len(written))
    for w in written:
        print("  " + w)


if __name__ == "__main__":
    main()
