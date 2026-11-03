#!/usr/bin/env python3
"""Build the SWC JAWS preview: Aquatics, Swimming Lessons, Aquatics FAQ and Contact, with every lap swim hour and closure
read live from Pool Relay by finder.js (#today, #week, data-live). Nothing about WHEN the pools are open is typed here,
except the site's own conflicting hours, quoted and labeled as its text; only rates, policies and facts about the water.
Run: python3 build.py"""
import hashlib, html, json

E = html.escape
V = {"swc": "JSJFJ9CDLOoPHTfA7ElM0N"}  # Pool Relay share token: SWC JAWS, lane by lane
SITE = "https://swcjaws.com/aquatics/"
POOLS = [
    dict(slug="swc", name="Southwestern College Wellness & Aquatics Complex", short="SWC JAWS",
         facility="Southwestern College Wellness & Aquatics Complex", area="Chula Vista", kind="yearRound",
         address="900 Otay Lakes Rd, Chula Vista, CA 91910", phone="(619) 421-6700 x5741", href="index.html"),
]

def live(mode, **kw):
    attrs = "".join(f' data-{k.replace("_", "-")}="{E(str(v))}"' for k, v in kw.items())
    return f'data-live="{mode}" data-view="{V["swc"]}" data-pool="swc"{attrs}'

MENU = [("Aquatics", "index.html", 0), ("Swimming Lessons", "swimming-lessons.html", 1), ("Swimming Lesson Schedule", None, 1),
        ("Aquatics FAQ", "aquatics-faq.html", 1), ("Fitness", None, 0), ("Tennis & Pickleball", None, 0),
        ("About", None, 0), ("Contact", "contact.html", 1), ("Membership", None, 0)]

VER = hashlib.sha1((open("finder.js").read() + open("style.css").read()).encode()).hexdigest()[:8]  # cache-busts both on change

def page(file, title, body):
    menu = "".join(f'<a class="{"sub" if sub else ""}{" here" if href == file else ""}" href="{href or "#"}">{E(label)}</a>'
                   for label, href, sub in MENU)
    doc = f"""<!doctype html>
<!-- UNOFFICIAL PREVIEW. Not a Southwestern College website. A mock-up of {SITE}
     with JAWS's three pools on one live Pool Relay schedule. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(title)} | SWC JAWS preview</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css?v={VER}">
</head>
<body>
<div class="preview-note"><b>Unofficial preview.</b> Not a Southwestern College page &mdash; a mock-up of <a href="{SITE}" target="_blank" rel="noopener noreferrer">swcjaws.com</a> with all three pools on one live schedule.</div>
<header class="site"><div class="hdr">
  <a class="brand" href="index.html"><small>Southwestern College</small><span>SWC JAWS</span></a>
  <div class="right"><div class="util"><span>Jaguar Aquatics Wellness &amp; Sports</span><span>(619) 482-6327</span><span>Become a Member</span></div>
    <nav aria-label="Main"><span>Fitness</span><span>Aquatics</span><span>Tennis &amp; Pickleball</span><span>About</span><span>Membership</span></nav></div>
</div></header>
<div class="page">
  <aside class="side"><h2>Aquatics</h2><nav aria-label="Aquatics">{menu}</nav></aside>
  <main class="main"><h1>{E(title)}</h1>{body}</main>
  <aside class="contact"><h2>Contact</h2>{CONTACT}</aside>
</div>
<footer class="site"><div class="in">
  <div><h4>Jaguar Aquatics Wellness &amp; Sports</h4><p>Southwestern College<br>900 Otay Lakes Rd, Chula Vista, CA 91910<br>(619) 482-6327 · swcwac@swccd.edu</p></div>
  <div><h4>About this preview</h4><p>Built to demonstrate embedded <a href="https://www.poolrelay.com" target="_blank" rel="noopener">Pool Relay</a> schedules. Not operated by or affiliated with Southwestern College. Schedule entered from swcjaws.com on November 2, 2026; which pool and lanes lap swim uses is our estimate, as are the lane counts.</p></div>
</div></footer>
<script>window.POOLS = {json.dumps(POOLS)};</script>
<script src="finder.js?v={VER}"></script>
</body>
</html>
"""
    open(file, "w").write(doc)

CONTACT = """<p><b>Pool</b>(619) 421-6700 x5741<br>Phone answered afternoons and evenings</p>
<p><b>Pool email</b>swcpoolinfo@gmail.com</p><p><b>Swim lessons</b>swcswim@swccd.edu</p>
<p><b>Pool rentals</b>jperez3@swccd.edu</p>
<p><b>Parking</b>Lot J, orange-striped stalls; $10/month permit.</p>"""

WEEK = f'<div id="week" data-view="{V["swc"]}" data-pool="swc" data-pools="Fast Pool|Flex Pool|Teaching Pool"><p class="muted">Loading the week…</p></div>'
LANES = (f'<div class="frame"><iframe src="https://www.poolrelay.com/embed/{V["swc"]}" height="820" '
         f'title="SWC JAWS, lane by lane" loading="lazy"></iframe></div>')
LAP = live("hours", format="dl", title="Open Lap Swim", whole=0)

# ── Aquatics ─────────────────────────────────────────────────────────────────
page("index.html", "Aquatics", f"""
    <p class="lede">JAWS features the largest aquatics complex in the San Diego region: two Olympic-size pools and a warm-water instructional
      pool, home to the Jaguar swim and water polo teams and SOL Aquatics. Every time on these pages comes from the pools' live schedule, so when
      JAWS changes it, these pages change with it.</p>
    <div class="top2">
      <section class="now" aria-live="polite"><h2>Right now</h2>
        <div id="today" data-view="{V['swc']}" data-pool="swc"><p class="muted">Loading today’s schedule…</p></div></section>
      <aside class="hours"><h2>Open lap swim</h2>
        <div {LAP}><p class="muted">…</p></div>
        <div class="adjusted" {live("closures")} hidden></div>
        <p class="small muted" style="margin:6px 0 0">Reserve a lane by calling the front desk, then pick up a lane pass there.</p>
      </aside>
    </div>
    <h2>This week, pool by pool</h2>
    {WEEK}
    <h2>Lane by lane</h2>
    <p class="small muted">Pick a day to see who is in each lane of each pool.</p>
    {LANES}
    <h2>The pools</h2>
    <div class="facts">
      <div><h3>Fast Pool</h3><ul><li>50 meters, deep throughout</li><li>Competition swimming and water polo</li><li>Jaguar meets and games</li></ul></div>
      <div><h3>Flex Pool</h3><ul><li>50 meters, variable depth</li><li>Diving, PE, recreation and instruction</li><li>A bulkhead splits it between programs</li></ul></div>
      <div><h3>Teaching Pool</h3><ul><li>Warm-water instructional pool</li><li>Swim lessons and adaptive therapy</li></ul></div>
    </div>
    <p class="small muted">More than 1 million gallons of water, heated to 74–80°F. Opened January 2018.</p>
    <h2>Swimming pool policies</h2>
    <ul class="small"><li>Swimming only when a lifeguard is on duty; follow lifeguards' directions.</li>
      <li>Bathing suits, board shorts or rash guards only; no cotton or cutoffs. No deck changing.</li>
      <li>Sunscreen 15 minutes before entering; swim diapers required for children not toilet trained.</li>
      <li>No somersaults or back dives from the deck, blocks or bulkhead; no hanging on lane lines. Starting blocks are not for recreational use.</li>
      <li>No glass on deck. Staff may close parts of the pool in bad weather.</li></ul>

    <div class="replaces">
      <h2>What this replaces</h2>
      <ul>
        <li><b>Three sets of pool hours.</b> The Aquatics page lists open lap swim as "M/W/Th 5:30 AM – 6:00 PM, T/F 5:30 AM – 7:00 PM, Sa 7:00 AM –
          1:00 PM", while the same page's footer says "Monday &amp; Wednesday 5:30 AM – 6:00 PM, Tuesday &amp; Thursday 5:30 AM – 7:00 PM, Friday
          5:30 AM – 8:00 PM", and the Contact page says "Monday – Friday 5:30 AM – 7:00 PM". (All quoted from swcjaws.com.) Here there is one
          schedule, and every page reads it.</li>
        <li><b>Which pool?</b> Three pools, and lap swim never says which one or how many lanes. Here every booking names its pool and lanes.</li>
        <li><b>Lane reservations by phone.</b> To reserve a lane you call the front desk, and the line is answered only in the afternoon and evening.
          Here swimmers can see the open lanes before they call.</li>
        <li><b>Lessons only inside a booking widget.</b> Swim lesson times live in the Mindbody widget, day by day. Here they can sit on the same
          calendar as lap swim.</li>
        <li><b>Teams off the page.</b> The Jaguar teams, SOL Aquatics swim, water polo, dive and masters all practice here, but none of their
          times are on the site. Here they can be one schedule, so lap swimmers know what's coming.</li>
        <li><b>Holiday hours as a growing list.</b> The Contact page lists closures going back to 2023. Here a closure appears on its day and
          disappears when it's past.</li>
      </ul>
    </div>
""")

# ── Swimming Lessons ─────────────────────────────────────────────────────────
page("swimming-lessons.html", "Swimming Lessons", f"""
    <p class="lede">Affordable, safe, quality swimming lessons whether you are new to the world of swimming or an experienced water enthusiast,
      for ages 3 to adult.</p>
    <ul><li>New sessions start monthly</li><li>Progressive program from beginner to swim team levels</li><li>Low instructor-to-student ratio:
      5:1 for ages 3–5, 6:1 or 8:1 for older children</li><li>Heated outdoor pools</li><li>Strong focus on technique at all levels</li>
      <li>All instructors are American Red Cross Water Safety Instructors</li><li>Private 30-minute lessons by availability</li></ul>
    <p>Register by emailing swcswim@swccd.edu or stop by the Front Desk. Lessons break for Southwestern College district and federal holidays,
      with no make-ups.</p>
    <div class="adjusted" {live("closures")} hidden></div>
    <h2>Teaching Pool and everything around it</h2>
    <p class="small muted" style="margin-top:0">Lesson times aren't on this schedule yet; once JAWS enters them, they show up here and on the lane-by-lane view.</p>
    {LANES}
""")

# ── Aquatics FAQ ─────────────────────────────────────────────────────────────
FAQ = [("Can I make a swimming lane reservation in advance?", "Yes. Call the front desk to reserve, then stop by to pick up a swimming lane pass. The lane-by-lane calendar below shows which lanes are booked."),
       ("Can I rent out a pool for a special event?", "Yes, through Jaguar Aquatics Wellness & Sports. Email jperez3@swccd.edu or swcswim@swccd.edu."),
       ("Do you have lockers?", "Day-use lockers are free; items can't be left overnight. Monthly locker rentals are $10/month at the Front Desk."),
       ("Is the pool heated?", "Yes, 74–80°F."),
       ("Will there be a lifeguard on duty?", "Always. No one is allowed in the water without a certified lifeguard on duty."),
       ("Does Southwestern College have a swim club or Masters program?", "Yes: SOL Aquatics, with swim, water polo, dive and masters."),
       ("Is there a SWC JAWS app?", "Yes, free on Google Play and the App Store, for booking classes, checking schedules and managing your membership.")]
faq = "".join(f"<h3>{E(q)}</h3><p>{E(a)}</p>" for q, a in FAQ)
page("aquatics-faq.html", "Aquatics FAQ", f"""
    <p class="lede">Have a question about what we offer in our Aquatics program and what you can expect at JAWS?</p>
    {faq}
    <h2>Open lap swim</h2>
    <div {LAP}><p class="muted">…</p></div>
    <h2>Lane by lane</h2>
    {LANES}
""")

# ── Contact ──────────────────────────────────────────────────────────────────
page("contact.html", "Contact", f"""
    <p class="lede">We are located inside the Wellness &amp; Aquatics Complex on the Southwestern College campus, at the corner of East H Street
      and Otay Lakes Road.</p>
    <div class="top2">
      <aside class="hours"><h2>Pool hours</h2>
        <div {live("hours", format="dl", whole=1)}><p class="muted">…</p></div>
        <div class="adjusted" {live("exceptions", title="Open Lap Swim")} hidden></div>
      </aside>
      <aside class="hours"><h2>Coming closures</h2>
        <div {live("closures", label="Closed", empty="None scheduled")}><p class="muted">…</p></div>
      </aside>
    </div>
    <p>Questions about tours, your membership account, or general feedback: swcwac@swccd.edu or (619) 482-6327. Pool questions:
      swcpoolinfo@gmail.com or (619) 421-6700 x5741.</p>
""")
print("built 4 pages, assets", VER)
