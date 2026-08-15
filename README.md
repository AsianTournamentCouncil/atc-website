# Asian Tournament Council (ATC) — Official Website

Static, no-build website for **asiantournamentcouncil.github.io/atc-website**.
20 pages, plain HTML/CSS/JS — no framework, no server required.

## Structure

```
index.html            Home
about.html             About ATC
mission.html           Mission & Vision
what-we-do.html        What ATC Does
leadership.html        Leadership
ceo.html                CEO Profile
management.html        Management Structure
regions.html            Countries & Regions
tournaments.html       Tournament System
title-wars.html         ATC Title Wars — Season 1
community.html         Community Network
partners.html           Partner / Allied Communities
complaints.html         Complaint System
evidence.html            Evidence System
fairness.html            Fairness & Transparency
rules.html               Rules & Policies
news.html                News & Announcements
contact.html             Contact
privacy.html             Privacy Policy
terms.html               Terms & Conditions

css/style.css           All styling (design tokens at the top)
js/script.js             Mobile nav toggle + contact form
assets/                  Logo, favicon, Open Graph image
sitemap.xml               For Google Search Console
robots.txt                 Points crawlers to the sitemap
build.py                   Regenerates every .html file from templates
```

## Editing content

All page text lives inside **build.py** (not directly in the .html files).
To change anything — CEO bio, tournament details, contact info, a whole new
page — edit the relevant section in `build.py`, then regenerate:

```bash
python3 build.py
```

This overwrites all 20 `.html` files, `sitemap.xml`, and `robots.txt` from
the templates. Never hand-edit the `.html` files directly — those edits will
be lost the next time `build.py` runs. (If you'd rather hand-edit HTML going
forward, that's fine too — just stop running build.py after that point.)

## Editing design

Colors, fonts, spacing, and the "seal/plaque" visual style are all defined
as CSS variables at the top of `css/style.css` under `:root`.

## Moving to a custom domain later

All internal links and asset paths are **relative** (`about.html`,
`css/style.css`, etc.), so the site works unchanged whether it's served at
`asiantournamentcouncil.github.io/atc-website/` or at a future custom domain
root. Only two things need updating when a domain is purchased:

1. In `build.py`, change the `DOMAIN` variable at the top to the new domain.
2. Run `python3 build.py` again, then add a `CNAME` file (see GitHub's docs
   on custom domains for Pages) and update the domain in GitHub repo Settings → Pages.
