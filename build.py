#!/usr/bin/env python3
"""
Static site generator for the ATC — Asian Tournament Council website.
Run: python3 build.py
Outputs finished .html files into the same directory (repo root),
using relative asset/link paths so the site works both at a GitHub
Pages project URL (username.github.io/repo-name/) and at a future
custom domain root.
"""
import json

DOMAIN = "https://asiantournamentcouncil.github.io/atc-website"
ORG_NAME = "Asian Tournament Council"
ORG_SHORT = "ATC"
EMAIL = "tgcbal3472@gmail.com"
YOUTUBE = "https://youtube.com/@atccouncil"
DISCORD = "https://discord.gg/yZr3uap9"
CEO_NAME = "Pain FC"
PHONES = ["+92 317 3124405", "+62 821-3119-912", "0310 1452726"]

# (href, label) standalone items + grouped dropdowns
NAV_STANDALONE_HOME = ("index.html", "Home")
NAV_GROUPS = [
    ("Organization", [
        ("about.html", "About ATC"),
        ("mission.html", "Mission & Vision"),
        ("what-we-do.html", "What ATC Does"),
    ]),
    ("Leadership", [
        ("leadership.html", "Leadership"),
        ("ceo.html", "CEO Profile"),
        ("management.html", "Management Structure"),
    ]),
    ("Competition", [
        ("regions.html", "Countries & Regions"),
        ("tournaments.html", "Tournament System"),
        ("title-wars.html", "ATC Title Wars"),
    ]),
    ("Community", [
        ("community.html", "Community Network"),
        ("partners.html", "Partner Communities"),
    ]),
    ("Trust & Safety", [
        ("complaints.html", "Complaint System"),
        ("evidence.html", "Evidence System"),
        ("fairness.html", "Fairness & Transparency"),
        ("rules.html", "Rules & Policies"),
    ]),
]
NAV_TAIL = [("news.html", "News"), ("contact.html", "Contact")]

ALL_PAGES = [NAV_STANDALONE_HOME]
for _, items in NAV_GROUPS:
    ALL_PAGES += items
ALL_PAGES += NAV_TAIL
ALL_PAGES += [("privacy.html", "Privacy Policy"), ("terms.html", "Terms & Conditions")]


def org_schema(extra=None):
    data = {
        "@context": "https://schema.org",
        "@type": "SportsOrganization",
        "name": ORG_NAME,
        "alternateName": ORG_SHORT,
        "url": DOMAIN + "/",
        "logo": DOMAIN + "/assets/logo-512.png",
        "description": "Asian Tournament Council (ATC) is an Asian esports tournament organization that connects Free Fire tournament organizers and competitive communities across Pakistan, India, Bangladesh, Nepal and other Asian countries.",
        "foundingLocation": "Asia",
        "sameAs": [YOUTUBE, DISCORD],
        "email": EMAIL,
        "founder": {
            "@type": "Person",
            "name": CEO_NAME,
            "jobTitle": "Founder & CEO"
        }
    }
    if extra:
        data.update(extra)
    return json.dumps(data, indent=2, ensure_ascii=False)


def head(title, description, path, extra_schema=None):
    canonical = f"{DOMAIN}/" if path == "index.html" else f"{DOMAIN}/{path}"
    schema = org_schema(extra_schema)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{ORG_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/assets/og-image.png">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{DOMAIN}/assets/og-image.png">

<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="assets/logo-180.png">
<link rel="stylesheet" href="css/style.css">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700&family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script type="application/ld+json">
{schema}
</script>
</head>
"""


def nav_links_html(active):
    parts = []
    href, label = NAV_STANDALONE_HOME
    cur = ' aria-current="page"' if href == active else ""
    parts.append(f'<a href="{href}"{cur}>{label}</a>')

    for group_name, items in NAV_GROUPS:
        is_active_group = any(h == active for h, _ in items)
        link_parts = []
        for h, l in items:
            cur_attr = ' aria-current="page"' if h == active else ""
            link_parts.append(f'<a href="{h}"{cur_attr}>{l}</a>')
        links = "\n          ".join(link_parts)
        marker = ' style="color:var(--gold-bright);"' if is_active_group else ""
        parts.append(f"""<details class="nav-group">
        <summary{marker}>{group_name}</summary>
        <div class="dropdown">
          {links}
        </div>
      </details>""")

    for href, label in NAV_TAIL:
        cur = ' aria-current="page"' if href == active else ""
        parts.append(f'<a href="{href}"{cur}>{label}</a>')

    return "\n        ".join(parts)


def header(active):
    return f"""<header class="site-header">
  <nav class="nav">
    <a href="index.html" class="brand">
      <img src="assets/logo-192.png" alt="ATC crest logo">
      <span class="brand-name">Asian Tournament<br>Council<small>ATC · UNITING ASIA. BUILDING LEGENDS.</small></span>
    </a>
    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">☰</button>
    <div class="nav-links">
        {nav_links_html(active)}
    </div>
  </nav>
</header>
"""


def footer():
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">
          <img src="assets/logo-192.png" alt="ATC crest logo">
          <div style="font-family:var(--serif);font-size:1rem;">Asian Tournament Council</div>
        </div>
        <p class="footer-tag">ONE ASIA. ONE STANDARD. FAIR COMPETITION.</p>
      </div>
      <div>
        <h4>Organization</h4>
        <ul>
          <li><a href="about.html">About ATC</a></li>
          <li><a href="mission.html">Mission &amp; Vision</a></li>
          <li><a href="what-we-do.html">What ATC Does</a></li>
          <li><a href="leadership.html">Leadership</a></li>
          <li><a href="ceo.html">CEO Profile</a></li>
          <li><a href="management.html">Management Structure</a></li>
        </ul>
      </div>
      <div>
        <h4>Competition</h4>
        <ul>
          <li><a href="regions.html">Countries &amp; Regions</a></li>
          <li><a href="tournaments.html">Tournament System</a></li>
          <li><a href="title-wars.html">ATC Title Wars</a></li>
          <li><a href="community.html">Community Network</a></li>
          <li><a href="partners.html">Partner Communities</a></li>
        </ul>
      </div>
      <div>
        <h4>Trust &amp; Contact</h4>
        <ul>
          <li><a href="complaints.html">Complaint System</a></li>
          <li><a href="evidence.html">Evidence System</a></li>
          <li><a href="fairness.html">Fairness &amp; Transparency</a></li>
          <li><a href="rules.html">Rules &amp; Policies</a></li>
          <li><a href="news.html">News</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Asian Tournament Council (ATC). All rights reserved.</span>
      <span><a href="privacy.html">Privacy Policy</a> · <a href="terms.html">Terms &amp; Conditions</a></span>
    </div>
  </div>
</footer>
<script src="js/script.js"></script>
</body>
</html>
"""


def page(path, title, description, active, body, extra_schema=None):
    html = head(title, description, path, extra_schema) + "<body>\n" + header(active) + body + "\n" + footer()
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", path)


def page_head(eyebrow, h1, sub, crumb):
    return f"""<section class="page-head">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Home</a> / {crumb}</div>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{h1}</h1>
    <p class="lead" style="max-width:680px;">{sub}</p>
  </div>
</section>
"""


# ================= INDEX =================
index_body = f"""
<section class="hero">
  <div class="container">
    <img src="assets/logo-256.png" alt="ATC crest — lion, crown and shield" class="hero-crest">
    <div class="eyebrow" style="justify-content:center;">UNITING ASIA · BUILDING LEGENDS</div>
    <h1>Asian Tournament Council</h1>
    <p class="lead">One trusted tournament network across Asia — where organizers work together to make
    competitive Free Fire fair, transparent, and connected.</p>
    <div class="btn-row" style="justify-content:center;">
      <a href="about.html" class="btn btn-primary">Read the Manifesto</a>
      <a href="{DISCORD}" class="btn" rel="noopener">Join the Discord</a>
    </div>

    <div class="stat-strip">
      <div class="stat"><span class="num">4+</span><span class="label">Asian Countries</span></div>
      <div class="stat"><span class="num">1</span><span class="label">Shared Ban System</span></div>
      <div class="stat"><span class="num">6 YRS</span><span class="label">Leadership Experience</span></div>
      <div class="stat"><span class="num">100%</span><span class="label">Evidence-Based Review</span></div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="callout" style="display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap;">
      <p><strong>Now open — ATC Title Wars, Season 1.</strong> Free entry. Clash Squad, Mobile &amp; PC. 50 slots each. No prize pool — teams compete for official ATC titles.</p>
      <a href="title-wars.html" class="btn btn-primary" style="flex-shrink:0;">View Title Wars →</a>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="eyebrow">WHY ATC EXISTS</div>
    <h2>A council, not just a community</h2>
    <p class="lead" style="max-width:720px;">ATC is not another Free Fire community — it's a coordination
    layer between the organizers who already run Asia's tournaments. Four problems drove us to build it.</p>

    <div class="grid grid-3" style="margin-top:44px;">
      <div class="card">
        <div class="hex">01</div>
        <h3>One Ban System</h3>
        <p>Players caught cheating shouldn't be able to erase their record by switching community or country. ATC lets organizers share verified, evidence-backed history.</p>
      </div>
      <div class="card">
        <div class="hex">02</div>
        <h3>Tournament Reach</h3>
        <p>International opportunities often stay inside a few well-connected communities. ATC connects organizers so announcements reach underrated teams too.</p>
      </div>
      <div class="card">
        <div class="hex">03</div>
        <h3>Fairness for Players</h3>
        <p>A structured, evidence-based way for players to report unjust bans or decisions — every case reviewed on its merits, not on politics.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="eyebrow">THE COUNCIL</div>
    <h2>Built for organizers, players, and the future of competitive Free Fire in Asia</h2>
    <p class="lead" style="max-width:720px;">ATC unites organizers from Pakistan, India, Bangladesh, Nepal, and other Asian countries under one platform — one standard for competitive integrity.</p>
    <div class="btn-row">
      <a href="mission.html" class="btn">Mission &amp; Vision</a>
      <a href="rules.html" class="btn">Rules &amp; Policies</a>
      <a href="ceo.html" class="btn">Meet the CEO</a>
    </div>
  </div>
</section>
"""
page("index.html",
     "Asian Tournament Council (ATC) — Official Site",
     "Asian Tournament Council (ATC) is an Asian esports tournament organization connecting Free Fire tournament organizers and competitive communities across Pakistan, India, Bangladesh, Nepal and beyond.",
     "index.html", index_body)

# ================= ABOUT =================
about_body = page_head("ABOUT ATC", "One trusted tournament network for Asia",
    "What the Asian Tournament Council is, who it serves, and the problem it was built to solve.",
    "About") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2" style="align-items:start;">
      <div>
        <h2>What is ATC?</h2>
        <p class="lead">Asian Tournament Council (ATC) is an Asian esports tournament organization focused on
        connecting tournament organizers and competitive Free Fire communities across Asia.</p>
        <p>ATC is not just another Free Fire community. It exists to build one trusted tournament network
        across the region, where organizers cooperate instead of operating in isolation — making the
        competitive scene fairer, more transparent, and better connected.</p>
        <p>The council's founding goal is to unite organizers from Pakistan, India, Bangladesh, Nepal, and
        other Asian countries under a single platform, with shared standards for player conduct and
        tournament integrity.</p>
      </div>
      <div>
        <h2>What ATC does</h2>
        <ul class="rule-list">
          <li><span class="n">→</span><div><h3>Connects organizers</h3><p>A shared network so tournament organizers across countries can coordinate instead of working in silos.</p></div></li>
          <li><span class="n">→</span><div><h3>Organizes competitive play</h3><p>Shared standards that bring more structure to how Asian Free Fire tournaments are run and announced.</p></div></li>
          <li><span class="n">→</span><div><h3>Promotes fairness &amp; transparency</h3><p>An evidence-based process for reviewing disputes, bans, and reports of misconduct.</p></div></li>
          <li><span class="n">→</span><div><h3>Improves cooperation</h3><p>A common ground for organizers to work together rather than compete for control of the scene.</p></div></li>
        </ul>
        <a href="what-we-do.html" class="btn" style="margin-top:8px;">See the full breakdown →</a>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="eyebrow">ORGANIZATION TYPE</div>
    <h2>A council of organizers, for organizers and players</h2>
    <p class="lead" style="max-width:720px;">ATC is structured as a coordinating council rather than a single
    tournament brand — its role is to connect the people who already run Asia's Free Fire competitive scene,
    under one shared standard.</p>
    <div class="btn-row">
      <a href="mission.html" class="btn btn-primary">Read the full Mission &amp; Vision</a>
    </div>
  </div>
</section>
"""
page("about.html",
     "About ATC — Asian Tournament Council",
     "Asian Tournament Council (ATC) connects Free Fire tournament organizers across Pakistan, India, Bangladesh, Nepal and other Asian countries under one fair, transparent standard.",
     "about.html", about_body)


# ================= MISSION =================
mission_body = page_head("MISSION & VISION", "One Asia. One Standard. Fair Competition.",
    "The principles behind ATC — why it was founded and what it is working toward.",
    "Mission") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2">
      <div class="card">
        <div class="hex">M</div>
        <h3>Mission</h3>
        <p>To unite Asian Free Fire tournament organizers on one platform — sharing verified player
        history, coordinating tournament announcements, and holding the competitive scene to a single,
        transparent standard of fairness.</p>
      </div>
      <div class="card">
        <div class="hex">V</div>
        <h3>Vision</h3>
        <p>To make ATC the most trusted Free Fire tournament community in Asia — a place where fairness,
        transparency, and cooperation come before personal interests.</p>
      </div>
    </div>

    <div class="divider" style="margin-top:70px;"><span class="mark"></span></div>

    <h2 style="text-align:center;">What we're solving</h2>
    <ul class="rule-list" style="max-width:800px;margin:32px auto 0;">
      <li><span class="n">01</span><div><h3>One Ban System Across Asia</h3><p>Players caught using panels, cheats, or other unfair methods often simply move to another community or country and keep playing, because organizers elsewhere don't know their history. ATC lets organizers share verified, evidence-backed information so proven misconduct can't be erased by switching communities.</p></div></li>
      <li><span class="n">02</span><div><h3>Better Tournament Connectivity</h3><p>Many international tournaments never reach underrated teams because information stays within a few communities. Connecting organizers across countries means announcements reach more teams — giving everyone a fair shot at international events.</p></div></li>
      <li><span class="n">03</span><div><h3>Fairness for Every Player</h3><p>In some communities, players are unfairly banned or treated unjustly. ATC gives players a proper way to report unfair decisions with valid proof, with every case reviewed fairly — protecting honest players and competitive integrity.</p></div></li>
      <li><span class="n">04</span><div><h3>Protecting Players &amp; Teams from Scams</h3><p>Some players and teams face scams, false promises, or unfair treatment from certain organizers. ATC promotes honesty and accountability — reports of scams or misconduct backed by valid evidence are reviewed, and confirmed cases lead to action under community rules.</p></div></li>
    </ul>
  </div>
</section>

<section class="section-alt">
  <div class="container" style="text-align:center;">
    <div class="eyebrow" style="justify-content:center;">THE STANDARD</div>
    <h2>A community built for organizers, players, and the future of competitive Free Fire in Asia</h2>
    <div class="btn-row" style="justify-content:center;">
      <a href="{DISCORD}" class="btn btn-primary" rel="noopener">Support ATC on Discord</a>
    </div>
  </div>
</section>
"""
page("mission.html",
     "Mission & Vision — Asian Tournament Council",
     "ATC's mission: one shared ban system, better tournament connectivity, fairness for every player, and protection from scams — across Asia's Free Fire competitive scene.",
     "mission.html", mission_body)

# ================= WHAT WE DO =================
what_body = page_head("WHAT ATC DOES", "What ATC Does",
    "The concrete functions ATC performs for organizers, teams, and players across Asia.",
    "What ATC Does") + """
<section class="tight">
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="hex">01</div>
        <h3>Organizer Network</h3>
        <p>Connects tournament organizers across Asian countries so they can coordinate schedules, share verified player history, and back each other's decisions.</p>
      </div>
      <div class="card">
        <div class="hex">02</div>
        <h3>Shared Ban System</h3>
        <p>A player proven guilty of cheating in one part of the network can't simply reappear in another community or country under the ATC umbrella.</p>
      </div>
      <div class="card">
        <div class="hex">03</div>
        <h3>Tournament Coordination</h3>
        <p>Runs official ATC events — such as ATC Title Wars — and helps distribute tournament announcements across the wider network.</p>
      </div>
      <div class="card">
        <div class="hex">04</div>
        <h3>Complaint &amp; Evidence Review</h3>
        <p>Provides a structured way for players and organizers to submit evidence-backed complaints, which are reviewed before any action is taken.</p>
      </div>
      <div class="card">
        <div class="hex">05</div>
        <h3>Fairness &amp; Transparency</h3>
        <p>Holds every case — bans, disputes, scam reports — to the same evidence-based standard, regardless of who is involved.</p>
      </div>
      <div class="card">
        <div class="hex">06</div>
        <h3>Community Growth</h3>
        <p>Works to bring more Asian countries and organizer communities into the network as participation grows.</p>
      </div>
    </div>
    <div class="btn-row">
      <a href="tournaments.html" class="btn">Tournament System</a>
      <a href="complaints.html" class="btn">Complaint System</a>
      <a href="evidence.html" class="btn">Evidence System</a>
    </div>
  </div>
</section>
"""
page("what-we-do.html",
     "What ATC Does — Asian Tournament Council",
     "The Asian Tournament Council (ATC) connects organizers, runs a shared ban system, coordinates tournaments, and reviews complaints and evidence across Asia's Free Fire scene.",
     "what-we-do.html", what_body)

# ================= LEADERSHIP =================
leadership_body = page_head("LEADERSHIP", "Leadership & Management",
    "The people responsible for ATC's direction, standards, and day-to-day coordination.",
    "Leadership") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="hex">★</div>
        <span class="tag">Founder &amp; CEO</span>
        <h3>{CEO_NAME}</h3>
        <p>Founder and CEO of Asian Tournament Council. Leads ATC's overall direction and standards.
        <a href="ceo.html">View full profile →</a></p>
      </div>
      <div class="card" style="opacity:0.6;">
        <div class="hex">·</div>
        <span class="tag">Executive Team</span>
        <h3>Vacant</h3>
        <p>No members officially appointed yet. This role will be filled in as ATC's structure develops.</p>
      </div>
      <div class="card" style="opacity:0.6;">
        <div class="hex">·</div>
        <span class="tag">Representatives</span>
        <h3>Vacant</h3>
        <p>Official country representatives will be listed here as ATC's regional network grows.</p>
      </div>
    </div>

    <div class="callout">
      <p><strong>Note:</strong> ATC only lists confirmed leadership with verified roles. See the full
      <a href="management.html">Management Structure</a> for every position and its current status.</p>
    </div>
  </div>
</section>
"""
page("leadership.html",
     "Leadership — Asian Tournament Council",
     "Meet the leadership of Asian Tournament Council (ATC), including Founder & CEO Pain FC.",
     "leadership.html", leadership_body)

# ================= CEO =================
ceo_body = page_head("CEO PROFILE", "Pain FC", "Founder & Chief Executive Officer, Asian Tournament Council.", "CEO") + f"""
<section class="tight">
  <div class="container">
    <div class="person">
      <div>
        <div class="avatar"><img src="assets/logo-512.png" alt="Pain FC — Founder and CEO of Asian Tournament Council"></div>
        <div class="person-meta">
          <div><span>Role</span><span>Founder &amp; CEO</span></div>
          <div><span>Organization</span><span>ATC</span></div>
          <div><span>Also leads</span><span>File Close</span></div>
          <div><span>Experience</span><span>6 years</span></div>
          <div><span>Contact</span><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
        </div>
      </div>
      <div>
        <span class="tag">Founder &amp; CEO — Asian Tournament Council</span>
        <h2>About {CEO_NAME}</h2>
        <p class="lead">{CEO_NAME} is the Founder and CEO of the Asian Tournament Council (ATC), and the
        leader of File Close, a recognized Pakistani Free Fire guild.</p>
        <p>{CEO_NAME} has been active in the competitive Free Fire scene for six years. As the leader of
        File Close, one of Pakistan's established Free Fire guilds, {CEO_NAME} has spent that time inside
        the day-to-day realities of the region's competitive community — which shaped the decision to
        found ATC: a shared standard for fairness, transparency, and cooperation between organizers across
        Asia.</p>
        <p>As Founder &amp; CEO, {CEO_NAME} sets ATC's overall direction, its rules framework, and its
        relationships with organizers across Pakistan, India, Bangladesh, Nepal, and other Asian countries.</p>

        <h3 style="margin-top:36px;">Official links</h3>
        <div class="btn-row">
          <a href="{YOUTUBE}" class="btn" rel="noopener">YouTube — @atccouncil</a>
          <a href="{DISCORD}" class="btn" rel="noopener">Discord</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""
page("ceo.html",
     "Pain FC — CEO, Asian Tournament Council",
     "Pain FC is the Founder and CEO of Asian Tournament Council (ATC) and leader of File Close, a Pakistani Free Fire guild, with 6 years in the competitive scene.",
     "ceo.html", ceo_body,
     extra_schema={"mainEntity": {"@type": "Person", "name": CEO_NAME, "jobTitle": "Founder & CEO", "worksFor": {"@type": "Organization", "name": ORG_NAME}}})

# ================= MANAGEMENT STRUCTURE =================
management_body = page_head("MANAGEMENT STRUCTURE", "Management Structure",
    "ATC's organizational roles and their current status.",
    "Management Structure") + f"""
<section class="tight">
  <div class="container">
    <ul class="rule-list">
      <li><span class="n">★</span><div><h3>Founder &amp; CEO — {CEO_NAME}</h3><p>Officially confirmed. Sets ATC's overall direction, standards, and rules framework. <a href="ceo.html">Full profile →</a></p></div></li>
      <li><span class="n">·</span><div><h3>Executive / Management Team — Vacant</h3><p>This role exists in ATC's structure but no members have been officially appointed yet.</p></div></li>
      <li><span class="n">·</span><div><h3>Department Heads — Vacant</h3><p>To be appointed as ATC's operations expand (e.g. tournaments, community, trust &amp; safety).</p></div></li>
      <li><span class="n">·</span><div><h3>Official Country Representatives — Vacant</h3><p>To be appointed for each participating country as ATC's regional network grows.</p></div></li>
    </ul>
    <div class="callout">
      <p><strong>Note:</strong> This page will be updated with real names and titles only once positions are
      officially appointed by ATC management. No placeholder names are used.</p>
    </div>
  </div>
</section>
"""
page("management.html",
     "Management Structure — Asian Tournament Council",
     "ATC's organizational structure: Founder & CEO Pain FC is currently the only officially confirmed leadership position.",
     "management.html", management_body)


# ================= REGIONS =================
regions_body = page_head("COUNTRIES & REGIONS", "Where ATC operates",
    "The Asian countries ATC currently connects — with room to grow.",
    "Regions") + """
<section class="tight">
  <div class="container">
    <h2>Founding countries</h2>
    <p class="lead" style="max-width:680px;">ATC's founding goal is to unite tournament organizers from these
    countries under one platform, with more Asian countries to follow.</p>
    <div class="region-list" style="margin-top:28px;">
      <span class="region-chip">🇵🇰 Pakistan</span>
      <span class="region-chip">🇮🇳 India</span>
      <span class="region-chip">🇧🇩 Bangladesh</span>
      <span class="region-chip">🇳🇵 Nepal</span>
      <span class="region-chip pending">+ More Asian countries — coming soon</span>
    </div>

    <div class="callout">
      <p><strong>For organizers:</strong> if you run a Free Fire tournament community in an Asian country not
      yet listed here and want to join the council, reach out via the <a href="contact.html">Contact page</a>.</p>
    </div>
  </div>
</section>
"""
page("regions.html",
     "Countries & Regions — Asian Tournament Council",
     "ATC currently connects Free Fire tournament organizers in Pakistan, India, Bangladesh, and Nepal, with more Asian countries joining over time.",
     "regions.html", regions_body)

# ================= TOURNAMENT SYSTEM =================
tournaments_body = page_head("TOURNAMENT SYSTEM", "Tournament System",
    "How ATC structures and coordinates tournaments across its network.",
    "Tournament System") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2" style="align-items:start;">
      <div>
        <h2>How ATC tournaments work</h2>
        <p class="lead">ATC coordinates tournaments across its organizer network rather than running events in
        isolation — so results, standards, and player records carry across the whole council.</p>
        <ul class="rule-list">
          <li><span class="n">→</span><div><h3>Council-run events</h3><p>Flagship tournaments, such as ATC Title Wars, are organized directly by ATC.</p></div></li>
          <li><span class="n">→</span><div><h3>Network-wide announcements</h3><p>Tournament information is shared across partner organizers so more teams across Asia can take part.</p></div></li>
          <li><span class="n">→</span><div><h3>Shared player standards</h3><p>The same ban system and evidence-based review applies to every ATC-coordinated tournament.</p></div></li>
        </ul>
      </div>
      <div class="card">
        <div class="hex">👑</div>
        <span class="tag">Flagship Event</span>
        <h3>ATC Title Wars — Season 1</h3>
        <p>Free-entry Clash Squad tournament, Mobile &amp; PC categories, 50 teams each. Teams compete for
        official ATC titles — no cash prize.</p>
        <a href="title-wars.html" class="btn btn-primary" style="margin-top:14px;">Full Title Wars details →</a>
      </div>
    </div>
  </div>
</section>
"""
page("tournaments.html",
     "Tournament System — Asian Tournament Council",
     "How ATC coordinates tournaments — including its flagship ATC Title Wars event — across its network of Free Fire organizers in Asia.",
     "tournaments.html", tournaments_body)

# ================= ATC TITLE WARS =================
title_wars_body = page_head("FLAGSHIP TOURNAMENT", "ATC Title Wars — Season 1",
    "Free Fire Clash Squad tournament by Asian Tournament Council. Free entry. Mobile & PC. No prize pool — teams compete for official ATC titles.",
    "ATC Title Wars") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2" style="align-items:start;">
      <div>
        <h2>Tournament information</h2>
        <ul class="rule-list">
          <li><span class="n">→</span><div><h3>Organized by</h3><p>Asian Tournament Council (ATC)</p></div></li>
          <li><span class="n">→</span><div><h3>Game mode</h3><p>Clash Squad (CS) only</p></div></li>
          <li><span class="n">→</span><div><h3>Categories</h3><p>Mobile Category (Mobile vs Mobile) · PC Category (PC vs PC)</p></div></li>
          <li><span class="n">→</span><div><h3>Slots</h3><p>50 Mobile teams · 50 PC teams</p></div></li>
          <li><span class="n">→</span><div><h3>Entry fee</h3><p>Free — 0</p></div></li>
          <li><span class="n">→</span><div><h3>Prize pool</h3><p>No prize pool, no cash prize. Teams compete for official ATC achievement titles instead.</p></div></li>
          <li><span class="n">→</span><div><h3>Start date &amp; match schedule</h3><p>To Be Announced</p></div></li>
          <li><span class="n">→</span><div><h3>Registration deadline</h3><p>To Be Announced</p></div></li>
          <li><span class="n">→</span><div><h3>Live streaming</h3><p>All matches will be streamed live. Platform/channel — To Be Announced.</p></div></li>
        </ul>
      </div>
      <div>
        <div class="card" style="margin-bottom:24px;">
          <div class="hex">?</div>
          <h3>Why is Title Wars free?</h3>
          <p>Season 1 is organized primarily to check community activity and participation across Asia —
          Pakistan, India, Bangladesh, Nepal, and other Asian countries. What ATC learns from the turnout
          will shape how it plans future competitions, which may include tournaments with prize pools,
          free-entry tournaments with prizes, and international events. These future formats are plans
          based on Season 1 participation — not confirmed or scheduled events.</p>
        </div>
        <div class="card">
          <div class="hex">👑</div>
          <h3>Official tournament titles</h3>
          <ul class="rule-list" style="margin-top:8px;">
            <li style="padding:12px 0;"><span class="n">👑</span><div><p style="margin:0;">ATC Asia No.1 Mobile Team</p></div></li>
            <li style="padding:12px 0;"><span class="n">👑</span><div><p style="margin:0;">ATC Asia No.1 PC Team</p></div></li>
            <li style="padding:12px 0;"><span class="n">🌍</span><div><p style="margin:0;">Top 10 Teams of every participating country</p></div></li>
            <li style="padding:12px 0;border-bottom:none;"><span class="n">⭐</span><div><p style="margin:0;">Tournament MVP — Best Player</p></div></li>
          </ul>
          <p style="margin-top:12px;font-size:0.85rem;">Mobile and PC titles are awarded separately. These
          are official achievement titles for this tournament — not permanent community ranks or permanent
          player/team positions.</p>
        </div>
      </div>
    </div>

    <div class="divider" style="margin-top:70px;"><span class="mark"></span></div>

    <div class="grid grid-2">
      <div>
        <h2>Slot booking / official contact</h2>
        <p>To book a slot or ask about registration, use the official tournament contact numbers below.</p>
        <ul class="rule-list">
          <li style="padding:14px 0;"><span class="n">☎</span><div><p style="margin:0;">{PHONES[0]}</p></div></li>
          <li style="padding:14px 0;"><span class="n">☎</span><div><p style="margin:0;">{PHONES[1]}</p></div></li>
          <li style="padding:14px 0;border-bottom:none;"><span class="n">☎</span><div><p style="margin:0;">{PHONES[2]}</p></div></li>
        </ul>
      </div>
      <div>
        <h2>Official slogan</h2>
        <p class="lead" style="font-family:var(--serif);font-size:1.4rem;color:var(--gold-bright);">
        "Fight the Best. Earn the Title. Make Your Name Across Asia."</p>
        <div class="btn-row">
          <a href="{DISCORD}" class="btn btn-primary" rel="noopener">Follow updates on Discord</a>
          <a href="{YOUTUBE}" class="btn" rel="noopener">ATC on YouTube</a>
        </div>
      </div>
    </div>
  </div>
</section>
"""
page("title-wars.html",
     "ATC Title Wars — Season 1 | Asian Tournament Council",
     "ATC Title Wars Season 1: a free-entry Clash Squad tournament by Asian Tournament Council, with Mobile and PC categories, 50 teams each, competing for official ATC titles.",
     "title-wars.html", title_wars_body)


# ================= COMMUNITY NETWORK =================
community_body = page_head("COMMUNITY NETWORK", "Community Network",
    "Where ATC's community lives, and how organizers can join the network.",
    "Community Network") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2">
      <div class="card">
        <div class="hex">D</div>
        <h3>Official Discord</h3>
        <p>The main hub for announcements, community discussion, and reports.</p>
        <a href="{DISCORD}" class="btn" rel="noopener" style="margin-top:12px;">Join Discord →</a>
      </div>
      <div class="card">
        <div class="hex">Y</div>
        <h3>Official YouTube</h3>
        <p>Announcements, updates, and future tournament coverage.</p>
        <a href="{YOUTUBE}" class="btn" rel="noopener" style="margin-top:12px;">@atccouncil →</a>
      </div>
    </div>

    <div class="callout" style="margin-top:44px;">
      <p><strong>Become a partner organizer:</strong> ATC is actively inviting tournament organizers and
      communities across Asia to join the network. <a href="contact.html">Get in touch</a> to start the
      conversation, or see <a href="partners.html">Partner Communities</a> for current partnership status.</p>
    </div>
  </div>
</section>
"""
page("community.html",
     "Community Network — Asian Tournament Council",
     "Join ATC's official Discord and YouTube, and learn how tournament organizers across Asia can join the ATC community network.",
     "community.html", community_body)

# ================= PARTNER / ALLIED COMMUNITIES =================
partners_body = page_head("PARTNER COMMUNITIES", "Partner / Allied Communities",
    "Organizer communities officially partnered with ATC.",
    "Partner Communities") + """
<section class="tight">
  <div class="container">
    <div class="callout">
      <p><strong>Coming soon.</strong> ATC does not currently have any officially confirmed partner or
      allied communities. This page will list them as official partnerships are announced.</p>
    </div>
    <h2>Want to partner with ATC?</h2>
    <p class="lead" style="max-width:680px;">If you organize Free Fire tournaments in an Asian country and
    want to join the council as a partner organizer, reach out through the Contact page.</p>
    <div class="btn-row">
      <a href="contact.html" class="btn btn-primary">Contact ATC</a>
    </div>
  </div>
</section>
"""
page("partners.html",
     "Partner / Allied Communities — Asian Tournament Council",
     "ATC currently has no officially confirmed partner or allied communities. This page will be updated as official partnerships are announced.",
     "partners.html", partners_body)

# ================= COMPLAINT SYSTEM =================
complaints_body = page_head("TRUST & SAFETY", "Complaint System",
    "How players, teams, and organizers can raise a complaint with ATC.",
    "Complaint System") + """
<section class="tight">
  <div class="container">
    <div class="grid grid-2" style="align-items:start;">
      <div>
        <h2>What you can report</h2>
        <ul class="rule-list">
          <li><span class="n">→</span><div><h3>Unfair bans</h3><p>Players who believe they were banned unjustly by an organizer within the network.</p></div></li>
          <li><span class="n">→</span><div><h3>Cheating / unfair play</h3><p>Panels, cheats, or other unfair methods used by an opposing player or team.</p></div></li>
          <li><span class="n">→</span><div><h3>Scams &amp; false promises</h3><p>Organizers or individuals who scam players or teams, or fail to honor commitments.</p></div></li>
          <li><span class="n">→</span><div><h3>Organizer misconduct</h3><p>Unfair or dishonest treatment by a tournament organizer within the ATC network.</p></div></li>
        </ul>
      </div>
      <div>
        <h2>How it works</h2>
        <ol style="color:var(--text-muted);padding-left:20px;">
          <li style="margin-bottom:14px;">Submit your complaint through the <a href="contact.html">Contact page</a>, including as much detail as possible.</li>
          <li style="margin-bottom:14px;">Attach supporting evidence — see the <a href="evidence.html">Evidence System</a> page for accepted formats.</li>
          <li style="margin-bottom:14px;">ATC reviews the complaint against the evidence provided — see <a href="fairness.html">Fairness &amp; Transparency</a>.</li>
          <li>If misconduct is confirmed, action is taken according to ATC's <a href="rules.html">Rules &amp; Policies</a>.</li>
        </ol>
      </div>
    </div>
    <div class="callout">
      <p><strong>No evidence, no action.</strong> Complaints without valid supporting evidence are not treated as findings of fact.</p>
    </div>
  </div>
</section>
"""
page("complaints.html",
     "Complaint System — Asian Tournament Council",
     "How to report unfair bans, cheating, scams, or organizer misconduct to Asian Tournament Council (ATC), and how complaints are reviewed.",
     "complaints.html", complaints_body)

# ================= EVIDENCE SYSTEM =================
evidence_body = page_head("TRUST & SAFETY", "Evidence System",
    "The standard ATC applies to evidence before acting on any complaint or ban.",
    "Evidence System") + """
<section class="tight">
  <div class="container">
    <div class="grid grid-3">
      <div class="card">
        <div class="hex">01</div>
        <h3>Evidence required</h3>
        <p>No ban, complaint, or dispute is acted on without valid supporting evidence submitted by the reporting party.</p>
      </div>
      <div class="card">
        <div class="hex">02</div>
        <h3>Reviewed on merit</h3>
        <p>Every piece of evidence is reviewed on its own merits — not on who is reporting or who is being reported.</p>
      </div>
      <div class="card">
        <div class="hex">03</div>
        <h3>Confirmed before action</h3>
        <p>Action is only taken once evidence confirms misconduct. Unproven claims do not result in bans or penalties.</p>
      </div>
    </div>
    <div class="callout">
      <p><strong>Submitting evidence:</strong> attach evidence directly when filing a report through the
      <a href="contact.html">Contact page</a>. Screenshots, clips, or recordings that clearly support the
      claim are the most useful.</p>
    </div>
  </div>
</section>
"""
page("evidence.html",
     "Evidence System — Asian Tournament Council",
     "How Asian Tournament Council (ATC) evaluates evidence before acting on bans, complaints, or disputes.",
     "evidence.html", evidence_body)

# ================= FAIRNESS & TRANSPARENCY =================
fairness_body = page_head("TRUST & SAFETY", "Fairness & Transparency",
    "The principles ATC applies to every decision, regardless of who is involved.",
    "Fairness & Transparency") + """
<section class="tight">
  <div class="container">
    <ul class="rule-list">
      <li><span class="n">01</span><div><h3>One standard for everyone</h3><p>The same evidence-based review process applies to every player, team, and organizer in the ATC network — no exceptions based on status or reputation.</p></div></li>
      <li><span class="n">02</span><div><h3>Evidence before judgment</h3><p>Decisions are based on submitted evidence, not accusations alone. See the <a href="evidence.html">Evidence System</a>.</p></div></li>
      <li><span class="n">03</span><div><h3>A path to appeal</h3><p>Players who believe a decision was unfair can report it with proof through the <a href="complaints.html">Complaint System</a>.</p></div></li>
      <li><span class="n">04</span><div><h3>Cooperation over control</h3><p>ATC's role is to coordinate organizers around shared standards — not to override individual communities without cause.</p></div></li>
    </ul>
  </div>
</section>
"""
page("fairness.html",
     "Fairness & Transparency — Asian Tournament Council",
     "The fairness and transparency principles behind every ATC decision — evidence-based review, equal standards, and a path to appeal.",
     "fairness.html", fairness_body)


# ================= RULES & POLICIES =================
rules_body = page_head("RULES & POLICIES", "Rules & Policies",
    "How ATC handles bans, disputes, and reports of unfair treatment.",
    "Rules") + """
<section class="tight">
  <div class="container">
    <ul class="rule-list">
      <li><span class="n">01</span><div><h3>Shared Ban System</h3><p>A player proven guilty of cheating, panel use, or other unfair methods — with valid evidence — is not permitted to continue competing by simply switching to another organizer or country inside the ATC network.</p></div></li>
      <li><span class="n">02</span><div><h3>Evidence Requirement</h3><p>No ban, report, or dispute is acted on without valid supporting evidence. Claims without proof are not treated as findings of fact.</p></div></li>
      <li><span class="n">03</span><div><h3>Fair Review Process</h3><p>Players who believe they were unfairly banned or penalized may report the decision with proof. Every case is reviewed on its merits before any action is taken or upheld.</p></div></li>
      <li><span class="n">04</span><div><h3>Scam &amp; Misconduct Reports</h3><p>Reports of scams, false promises, or unfair treatment by an organizer are reviewed the same way — evidence first, then a decision, then action under community rules if misconduct is confirmed.</p></div></li>
      <li><span class="n">05</span><div><h3>Cooperation Between Organizers</h3><p>Organizers in the ATC network agree to share verified player history and tournament information in good faith, to keep the standard consistent across countries.</p></div></li>
    </ul>

    <div class="callout">
      <p><strong>Report an issue:</strong> use the <a href="contact.html">Contact page</a> to submit a ban
      dispute, scam report, or organizer complaint along with supporting evidence.</p>
    </div>
  </div>
</section>
"""
page("rules.html",
     "Rules & Policies — Asian Tournament Council",
     "How ATC's shared ban system, evidence requirements, and fair review process work across its network of Free Fire tournament organizers.",
     "rules.html", rules_body)

# ================= NEWS =================
announcement_text = """
      <div class="post">
        <div class="post-meta">Announcement · ATC Management</div>
        <h2>Introducing ATC — Asian Tournament Council</h2>
        <p>We are proud to announce ATC (Asian Tournament Council).</p>
        <p>ATC is not just another Free Fire community. Our vision is to build one trusted tournament
        network across Asia, where organizers work together to make the competitive scene fair, transparent,
        and connected.</p>
        <p>Our goal is to unite organizers from Pakistan, India, Bangladesh, Nepal, and other Asian countries
        under one platform.</p>
        <h3>Why are we creating ATC?</h3>
        <p><strong>1. One Ban System Across Asia</strong> — Many players who are caught using panels, cheats,
        or other unfair methods simply move to another community or country and continue playing because
        organizers there don't know their history. ATC aims to solve this by allowing organizers to share
        verified information. If a player is proven guilty with valid evidence, they should not be able to
        continue competing by simply switching communities or countries.</p>
        <p><strong>2. Better Tournament Connectivity</strong> — Many international tournaments never reach
        underrated teams because the information stays within a few communities. By connecting organizers
        from different Asian countries, tournament announcements can reach more teams, giving everyone an
        equal opportunity to participate in international events.</p>
        <p><strong>3. Fairness for Every Player</strong> — We know that in some communities, players are
        unfairly banned or treated unjustly. ATC will promote transparency and accountability. Players will
        have a proper way to report unfair decisions with valid proof, and every case will be reviewed
        fairly. Our priority is to protect honest players and maintain competitive integrity.</p>
        <p><strong>4. Protecting Players and Teams from Scams &amp; Unfair Practices</strong> — Unfortunately,
        some players and teams experience scams, false promises, or unfair treatment from certain organizers.
        This damages trust within the competitive community. ATC is committed to promoting honesty,
        transparency, and accountability. If anyone reports a scam or unfair behavior with valid evidence,
        the case will be reviewed fairly. If the evidence confirms misconduct, appropriate action will be
        taken according to our community rules.</p>
        <h3>Our Vision</h3>
        <p>Our dream is to make ATC the most trusted Free Fire tournament community in Asia — a place where
        fairness, transparency, and cooperation come before personal interests. This is a community built for
        organizers, players, and the future of competitive Free Fire in Asia.</p>
        <p>We would be honored to have your support. Together, we can build something that benefits the
        entire Asian Free Fire esports community.</p>
        <p><em>Asian Tournament Council — One Asia. One Standard. Fair Competition.</em></p>
      </div>
"""

announcement_title_wars = """
      <div class="post">
        <div class="post-meta">Announcement · ATC Management</div>
        <h2>ATC Title Wars — Season 1 is open</h2>
        <p>ATC's first official tournament, <strong>ATC Title Wars — Season 1</strong>, is now open. Free
        entry, Clash Squad only, with separate Mobile and PC categories — 50 team slots each.</p>
        <p>There is no cash prize pool this season. Instead, teams compete for official ATC titles,
        including <strong>ATC Asia No.1 Mobile Team</strong>, <strong>ATC Asia No.1 PC Team</strong>,
        <strong>Top 10 Teams of every participating country</strong>, and <strong>Tournament MVP</strong>.</p>
        <p>Season 1 is primarily meant to gauge active, competitive team participation across Pakistan,
        India, Bangladesh, Nepal, and other Asian countries — the turnout will shape how ATC plans future
        tournaments, potentially including prize-pool and international events.</p>
        <p>Full details: <a href="title-wars.html">ATC Title Wars — Season 1</a>.</p>
      </div>
"""

news_body = page_head("NEWS & ANNOUNCEMENTS", "News & Announcements",
    "Official updates from ATC management.",
    "News") + f"""
<section class="tight">
  <div class="container" style="max-width:820px;">
    {announcement_title_wars}
    {announcement_text}
  </div>
</section>
"""
page("news.html",
     "News & Announcements — Asian Tournament Council",
     "Official announcements from ATC (Asian Tournament Council), including the launch of ATC Title Wars Season 1 and the council's founding statement.",
     "news.html", news_body)


# ================= CONTACT =================
phone_items = "\n          ".join(f'<li style="padding:10px 0;"><span class="n">☎</span><div><p style="margin:0;">{p}</p></div></li>' for p in PHONES)

contact_body = page_head("CONTACT", "Contact ATC",
    "Reach ATC management for reports, partnerships, or general questions.",
    "Contact") + f"""
<section class="tight">
  <div class="container">
    <div class="grid grid-2" style="align-items:start;">
      <div>
        <h2>Get in touch</h2>
        <p class="lead">For ban disputes, scam reports, organizer partnerships, or general questions.</p>
        <form id="contact-form" class="form-grid">
          <div>
            <label for="cf-name">Name</label>
            <input id="cf-name" type="text" required>
          </div>
          <div>
            <label for="cf-email">Email</label>
            <input id="cf-email" type="email" required>
          </div>
          <div>
            <label for="cf-subject">Subject</label>
            <select id="cf-subject">
              <option>General inquiry</option>
              <option>Ban dispute / report evidence</option>
              <option>Scam / organizer complaint</option>
              <option>Partnership / join as organizer</option>
              <option>ATC Title Wars — slot booking</option>
              <option>Press / media</option>
            </select>
          </div>
          <div>
            <label for="cf-message">Message</label>
            <textarea id="cf-message" required></textarea>
          </div>
          <button type="submit" class="btn btn-primary" style="justify-self:start;">Send message</button>
        </form>
        <p style="font-size:0.8rem;margin-top:10px;">This form opens your email app addressed to ATC —
        it does not send automatically from this page yet.</p>
      </div>
      <div>
        <div class="contact-cards">
          <div class="card">
            <div class="hex">@</div>
            <h3>Email</h3>
            <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          </div>
          <div class="card">
            <div class="hex">D</div>
            <h3>Discord</h3>
            <p><a href="{DISCORD}" rel="noopener">Join server</a></p>
          </div>
          <div class="card">
            <div class="hex">Y</div>
            <h3>YouTube</h3>
            <p><a href="{YOUTUBE}" rel="noopener">@atccouncil</a></p>
          </div>
          <div class="card">
            <div class="hex">★</div>
            <h3>CEO</h3>
            <p><a href="ceo.html">{CEO_NAME} — Founder &amp; CEO</a></p>
          </div>
        </div>
        <div class="card" style="margin-top:24px;">
          <div class="hex">☎</div>
          <h3>ATC Title Wars — Slot Booking</h3>
          <ul class="rule-list" style="margin-top:8px;">
            {phone_items}
          </ul>
        </div>
      </div>
    </div>
  </div>
</section>
"""
page("contact.html",
     "Contact — Asian Tournament Council",
     "Contact Asian Tournament Council (ATC) for ban disputes, scam reports, organizer partnerships, ATC Title Wars slot booking, or general questions.",
     "contact.html", contact_body,
     extra_schema={"mainEntity": {"@type": "ContactPage"}})

# ================= PRIVACY =================
privacy_body = page_head("LEGAL", "Privacy Policy",
    "How ATC collects, uses, and protects information submitted through this website.",
    "Privacy Policy") + f"""
<section class="tight">
  <div class="container" style="max-width:780px;">
    <p style="font-family:var(--mono);font-size:0.75rem;color:var(--text-faint);">Last updated: August 2026</p>

    <h2>1. Information we collect</h2>
    <p>When you use the contact form, report an issue, register for a tournament, or reach out via email,
    phone, or Discord, ATC may receive the information you choose to provide — such as your name, email
    address, phone number, Discord username, and the content of your message or report, including any
    evidence you submit.</p>

    <h2>2. How we use it</h2>
    <p>Information you submit is used to respond to your message, process tournament slot bookings, review
    ban disputes or scam reports, and coordinate with partner organizers where relevant to resolving a
    report. We do not sell your information to third parties.</p>

    <h2>3. Evidence submitted in reports</h2>
    <p>Evidence submitted as part of a ban dispute, scam report, or misconduct complaint is used solely for
    the purpose of reviewing that case and may be shared with relevant organizers within the ATC network
    where necessary to verify or act on a finding.</p>

    <h2>4. Third-party platforms</h2>
    <p>ATC's community operates partly through Discord and YouTube. Use of those platforms is also subject
    to their own respective privacy policies.</p>

    <h2>5. Contact</h2>
    <p>Questions about this policy can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

    <div class="callout">
      <p><strong>Note:</strong> this is a baseline policy template. Have it reviewed against your local
      regulations before you rely on it as your final published Privacy Policy.</p>
    </div>
  </div>
</section>
"""
page("privacy.html",
     "Privacy Policy — Asian Tournament Council",
     "Privacy Policy for the official Asian Tournament Council (ATC) website.",
     "privacy.html", privacy_body)

# ================= TERMS =================
terms_body = page_head("LEGAL", "Terms & Conditions",
    "The terms that govern participation in ATC's network and use of this website.",
    "Terms & Conditions") + f"""
<section class="tight">
  <div class="container" style="max-width:780px;">
    <p style="font-family:var(--mono);font-size:0.75rem;color:var(--text-faint);">Last updated: August 2026</p>

    <h2>1. About ATC</h2>
    <p>Asian Tournament Council (ATC) is an Asian esports tournament organization connecting tournament
    organizers and competitive Free Fire communities across Asia. By using this website or participating in
    ATC's network or tournaments (including ATC Title Wars), you agree to these terms.</p>

    <h2>2. Fair play &amp; the shared ban system</h2>
    <p>Players proven — with valid evidence — to have used cheats, panels, or other unfair methods may be
    banned from competing across the ATC network, not only with a single organizer. Bans are only enforced
    based on verified evidence, reviewed fairly.</p>

    <h2>3. Reporting &amp; evidence</h2>
    <p>Anyone submitting a ban dispute, scam report, or misconduct complaint must provide valid supporting
    evidence. False or bad-faith reports may themselves be subject to review.</p>

    <h2>4. Organizer conduct</h2>
    <p>Organizers participating in the ATC network are expected to act with honesty, transparency, and
    accountability toward players and teams. Confirmed misconduct — such as scams or false promises — may
    result in action under ATC's community rules.</p>

    <h2>5. Tournament participation</h2>
    <p>Entry to ATC-organized tournaments such as Title Wars is subject to the rules published on the
    relevant tournament page at the time of registration. Tournament titles awarded are achievement titles
    for that event and do not constitute a permanent rank or guarantee of future placement.</p>

    <h2>6. Changes</h2>
    <p>These terms may be updated as ATC's structure and rules develop. Continued use of ATC's platforms
    after changes means you accept the updated terms.</p>

    <h2>7. Contact</h2>
    <p>Questions about these terms can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>

    <div class="callout">
      <p><strong>Note:</strong> this is a baseline terms template. Have it reviewed before you rely on it as
      your final published Terms &amp; Conditions.</p>
    </div>
  </div>
</section>
"""
page("terms.html",
     "Terms & Conditions — Asian Tournament Council",
     "Terms and Conditions for the official Asian Tournament Council (ATC) website, network, and tournaments including ATC Title Wars.",
     "terms.html", terms_body)

# ================= SITEMAP + ROBOTS =================
urls = ""
for href, _ in ALL_PAGES:
    loc = f"{DOMAIN}/" if href == "index.html" else f"{DOMAIN}/{href}"
    urls += f"  <url><loc>{loc}</loc></url>\n"

sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>
"""
with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(sitemap)

robots = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
"""
with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots)

print(f"\nBuild complete. {len(ALL_PAGES)} pages generated.")
