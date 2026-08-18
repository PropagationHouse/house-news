# -*- coding: utf-8 -*-
"""Patch index.html, timeline.html, articles.json for Issue No. 52 (3 new dispatches)."""
import io, os, re, json

ROOT = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news"

def read(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return f.read()

def write(p, t):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(t)
    print("WROTE", p)

# ============================================================
# 1) INDEX.HTML
# ============================================================
idx = read(os.path.join(ROOT, "house-news", "index.html"))

# 1a) Issue number masthead + footer (No. 51 -> No. 52)
old51 = [
    '<div class="left"><span>Vol. III \u00b7 No. 51</span><span id="dateline">Monday, August 17, 2026</span></div>',
    '<span>Vol. III \u00b7 No. 51 \u00b7 August 17, 2026</span>',
]
new52 = [
    '<div class="left"><span>Vol. III \u00b7 No. 52</span><span id="dateline">Monday, August 17, 2026</span></div>',
    '<span>Vol. III \u00b7 No. 52 \u00b7 August 17, 2026</span>',
]
for o, n in zip(old51, new52):
    if o in idx:
        idx = idx.replace(o, n)
        print("ISSUE:", n[:60])
    else:
        print("WARN: not found issue string:", o[:60])

# 1b) Ticker: add 3 new items to BOTH halves (first half starts after '<div class="ticker-track">',
# second half begins at the repeat of "Unitree goes public")
ticker_items = [
    '<span>Unitree\u2019s \u201cSuperman\u201d jumps 2m and outruns humans \u2014 built in 3 months</span>',
    '<span>2,056 robots from 16 countries line up at Beijing\u2019s Ice Ribbon games</span>',
    '<span>San Mateo County votes to write the first US humanoid fleet permit rules</span>',
]
# The ticker block: find the two identical runs. Insert at top of first half and top of second half.
first_half_anchor = '<div class="ticker-track">\n'
second_half_anchor = first_half_anchor + ticker_items[0] if False else None
# Simpler: find first occurrence of 'Unitree goes public' span; insert before the first block
unitree_span = '<span>Unitree goes public in Shanghai'
first_pos = idx.find(unitree_span)
second_pos = idx.find(unitree_span, first_pos + 1)
assert first_pos != -1 and second_pos != -1, "ticker anchors not found"
insert1 = "\n".join(ticker_items) + "\n"
insert2 = "\n".join(ticker_items) + "\n"
idx = idx[:first_pos] + insert1 + idx[first_pos:]
# re-find second (now shifted by len(insert1))
second_pos = idx.find(unitree_span, first_pos + len(insert1) + 1)
idx = idx[:second_pos] + insert2 + idx[second_pos:]
print("TICKER: inserted 3 items x2 halves")

# 1c) Front grid — replace lead story with Superman
old_lead_start = idx.find('<div class="lead-story">')
old_lead_end = idx.find('</div>', idx.find('<div class="lead-story">'))  # not safe
# find the lead-story block end: it ends before '<div class="side-stories-left">'
lead_start = idx.find('<div class="lead-story">')
side_left_start = idx.find('<div class="side-stories-left">')
assert lead_start != -1 and side_left_start != -1 and side_left_start > lead_start
new_lead = '''<div class="lead-story">
    <a href="articles/superman-leaps.html" class="thumb"><img src="assets/images/superman-leaps-hero.jpg" alt="A humanoid robot frozen mid-leap in a dark arena"></a>
    <div class="kicker">Cover Story &middot; Robotics / Embodied AI</div>
    <h2><a href="articles/superman-leaps.html">Superman <em>Leaps</em></a></h2>
    <p class="dek">Unitree&rsquo;s new humanoid jumps two meters straight up and sprints faster than any human alive &mdash; built in just over three months. The humanoid race just stopped arguing about hands and started arguing about physics.</p>
    <div class="byline">By <strong>Propagation House</strong> &middot; 8 min read &middot; August 17, 2026</div>
  </div>'''
idx = idx[:lead_start] + new_lead + idx[side_left_start:]
print("FRONT: lead story replaced")

# 1d) Side stories — replace left with Beijing + San Mateo (keep one slot), right keep as-is
# Left column currently has breach + efficiency. We'll put Beijing + San Mateo there.
left_start = idx.find('<div class="side-stories-left">')
left_end = idx.find('<div class="side-stories-right">')
assert left_start != -1 and left_end != -1 and left_end > left_start
new_left = '''<div class="side-stories-left">
    <div class="ss-item">
      <div class="thumb sside"><img src="assets/images/beijing-games-hero.jpg" alt="Rows of humanoid robots on a running track inside a speed-skating oval"></div>
      <div class="kicker">Robotics &middot; Competition</div>
      <h3><a href="articles/beijing-games.html">The Games That <em>Grade</em> the Robots</a></h3>
      <p class="dek">2,056 humanoids from 16 countries run, kick, clean, and fight fires at Beijing&rsquo;s Ice Ribbon next week &mdash; many fully autonomous.</p>
      <div class="byline">By Propagation House &middot; 7 min</div>
    </div>
    <div class="ss-item">
      <div class="thumb sside"><img src="assets/images/san-mateo-permit-hero.jpg" alt="A humanoid robot before a municipal permit counter"></div>
      <div class="kicker">Regulatory &middot; Robotics</div>
      <h3><a href="articles/san-mateo-permit.html">The Permit That <em>Precedes</em> the Fleet</a></h3>
      <p class="dek">San Mateo County votes to write the first US permitting framework for commercial humanoid fleets &mdash; kill switches included.</p>
      <div class="byline">By Propagation House &middot; 8 min</div>
    </div>
  </div>'''
idx = idx[:left_start] + new_left + idx[left_end:]
print("FRONT: left side stories replaced")

# 1e) Bottom row — prepend new items? Keep existing 4; add Superman-related? The bottom row currently has chinese-ai, models-broke-out, design-tool, phantom-intern, rogue-agent, gemini-robotics, ai-designed-viruses.
# We'll leave bottom as-is (front grid has 1 lead + 2 left + 2 right = 5 fresh stories). Fine.

write(os.path.join(ROOT, "house-news", "index.html"), idx)

# ============================================================
# 2) TIMELINE.HTML
# ============================================================
tl = read(os.path.join(ROOT, "house-news", "timeline.html"))

# 2a) Add 3 nodes to ARTICLES array (insert before closing '];' of ARTICLES)
new_nodes = '''    {id:'superman-leaps', title:'Superman Leaps', href:'articles/superman-leaps.html', date:'2026-08-17', category:'Robotics', lens:'intelligence', read:'8 min', dek:'Unitree\\u2019s new humanoid jumps two meters straight up and sprints faster than any human alive \\u2014 built in just over three months.',
      tags:['unitree','humanoid','embodied-ai','athletics','china','frontier-models']},
    {id:'beijing-games', title:'The Games That Grade the Robots', href:'articles/beijing-games.html', date:'2026-08-17', category:'Robotics', lens:'intelligence', read:'7 min', dek:'2,056 humanoids from 16 countries line up at Beijing\\u2019s Ice Ribbon for the Second World Humanoid Robot Games \\u2014 many fully autonomous.',
      tags:['humanoid','robotics','competition','autonomy','china','embodied-ai']},
    {id:'san-mateo-permit', title:'The Permit That Precedes the Fleet', href:'articles/san-mateo-permit.html', date:'2026-08-17', category:'Regulatory', lens:'infrastructure', read:'8 min', dek:'San Mateo County becomes the first US jurisdiction to vote for a permitting framework for commercial humanoid fleets.',
      tags:['regulation','humanoid','permitting','labor','safety','embodied-ai']},
'''
# Insert before the line '  ];' that closes ARTICLES
# IMPORTANT: the last existing node must have a trailing comma, otherwise the
# graph JS dies with a syntax error and the whole node graph disappears.
articles_close = tl.find('  ];')
assert articles_close != -1
# Ensure the previous line ends with ',' (append one if missing)
prev_end = tl.rfind('\n', 0, articles_close)
prev_line = tl[prev_end:articles_close]
if not prev_line.rstrip().endswith(','):
    tl = tl[:articles_close] + ',' + tl[articles_close:]
tl = tl[:articles_close] + new_nodes + tl[articles_close:]
print("TIMELINE: 3 nodes added to ARTICLES")

# 2b) Add timeline-group items (visual timeline) — insert a new group after the header
# Find the first existing timeline-group (2026-08-15)
first_group = tl.find('<div class="timeline-group" data-date="2026-08-15">')
assert first_group != -1
new_group = '''<div class="timeline-group" data-date="2026-08-17">
    <div class="timeline-date">August 17, 2026</div>
    <div class="timeline-item" data-category="Robotics" data-lens="intelligence">
      <div class="ti-meta"><span>Robotics</span><span>Embodied AI</span><span>8 min</span></div>
      <h3><a href="articles/superman-leaps.html">Superman <em>Leaps</em></a></h3>
      <p class="ti-dek">Unitree\\u2019s new humanoid jumps two meters straight up and sprints faster than any human alive \\u2014 built in just over three months.</p>
    </div>
    <div class="timeline-item" data-category="Robotics" data-lens="intelligence">
      <div class="ti-meta"><span>Robotics</span><span>Competition</span><span>7 min</span></div>
      <h3><a href="articles/beijing-games.html">The Games That <em>Grade</em> the Robots</a></h3>
      <p class="ti-dek">2,056 humanoids from 16 countries line up at Beijing\\u2019s Ice Ribbon for the Second World Humanoid Robot Games.</p>
    </div>
    <div class="timeline-item" data-category="Regulatory" data-lens="infrastructure">
      <div class="ti-meta"><span>Regulatory</span><span>Robotics</span><span>8 min</span></div>
      <h3><a href="articles/san-mateo-permit.html">The Permit That <em>Precedes</em> the Fleet</a></h3>
      <p class="ti-dek">San Mateo County becomes the first US jurisdiction to vote for a permitting framework for commercial humanoid fleets.</p>
    </div>
  </div>
'''
tl = tl[:first_group] + new_group + tl[first_group:]
print("TIMELINE: new date group inserted")

# 2c) Bump total count 18 -> 21
tl = tl.replace('>18</div><div class="label">Total Dispatches', '>21</div><div class="label">Total Dispatches')
print("TIMELINE: count bumped to 21")

write(os.path.join(ROOT, "house-news", "timeline.html"), tl)

# ============================================================
# 3) ARTICLES.JSON
# ============================================================
aj_path = os.path.join(ROOT, "house-news", "content", "articles.json")
with io.open(aj_path, "r", encoding="utf-8") as f:
    aj = json.load(f)

new_entries = [
    {
        "title": "Superman Leaps",
        "kicker": "Robotics \u2013 Embodied AI",
        "dek": "Unitree\u2019s new humanoid jumps two meters straight up and sprints faster than any human alive \u2014 and the company says it built the whole thing in just over three months.",
        "author": "The Studio",
        "date": "2026-08-17",
        "category": "Robotics",
        "lens": "intelligence",
        "status": "published",
        "filename": "articles/superman-leaps.html",
        "read_time": "8 min",
        "summary": "Unitree previewed a humanoid that jumps 2m and hits 12.66 m/s \u2014 developed in three months, days before the Beijing games."
    },
    {
        "title": "The Games That Grade the Robots",
        "kicker": "Robotics \u2013 Competition",
        "dek": "More than two thousand humanoids from sixteen countries will run, kick, clean, and fight fires at Beijing\u2019s Ice Ribbon next week \u2014 many fully autonomous.",
        "author": "The Studio",
        "date": "2026-08-17",
        "category": "Robotics",
        "lens": "intelligence",
        "status": "published",
        "filename": "articles/beijing-games.html",
        "read_time": "7 min",
        "summary": "The Second World Humanoid Robot Games open at the Ice Ribbon with 51 events, 1,301 matches, and 2,056 robots from 16 countries."
    },
    {
        "title": "The Permit That Precedes the Fleet",
        "kicker": "Regulatory \u2013 Robotics",
        "dek": "San Mateo County just became the first American jurisdiction to vote for a permitting framework for commercial humanoid robots \u2014 kill switches, fire safety, and job-displacement tracking included.",
        "author": "The Studio",
        "date": "2026-08-17",
        "category": "Regulatory",
        "lens": "infrastructure",
        "status": "published",
        "filename": "articles/san-mateo-permit.html",
        "read_time": "8 min",
        "summary": "San Mateo County voted to draft the first US humanoid fleet permitting ordinance, including kill switches and job-displacement tracking."
    },
]

# Insert at the FRONT of published (newest first)
aj["published"] = new_entries + aj["published"]
with io.open(aj_path, "w", encoding="utf-8") as f:
    json.dump(aj, f, ensure_ascii=False, indent=2)
print("ARTICLES.JSON: 3 entries prepended to published")

print("ALL PATCHES DONE")
