# -*- coding: utf-8 -*-
"""Build Issue No. 52 — three dispatches, reusing the house article style block."""
import io, os

ROOT = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news"
SRC = os.path.join(ROOT, "house-news", "articles", "phantom-goes-public.html")

with io.open(SRC, "r", encoding="utf-8") as f:
    src = f.read()

# Extract ONLY the <style> block from the source (keeps fonts + house CSS)
style_start = src.find("<style>")
style_end = src.find("</style>") + len("</style>")
STYLE = src[style_start:style_end]

PROGRESS_JS = '<script>(function(){var bar=document.getElementById("progress");function update(){var h=document.documentElement;var scrolled=h.scrollTop/(h.scrollHeight-h.clientHeight);bar.style.width=(scrolled*100)+"%";}window.addEventListener("scroll",update,{passive:true});update();})();</script>'

def build(title, section_tag, kicker, h1, dek, byline, hero_img, hero_alt, caption,
          body, tags, related):
    return ("<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
            "<meta charset=\"UTF-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
            "<title>" + title + " - house</title>\n"
            + STYLE + "\n</head>\n<body>\n"
            '<div class="progress" id="progress"></div>\n'
            '<header class="masthead"><div class="logo"><a href="../index.html">house</a></div>'
            '<div class="section-tag">' + section_tag + '</div>'
            '<nav><a href="../index.html">Dispatches</a><a href="#">Studio</a><a href="#">Field Notes</a><a href="#">Index</a></nav></header>\n'
            '<div class="article-hero"><div class="kicker">' + kicker + '</div>'
            '<h1>' + h1 + '</h1>'
            '<p class="dek">' + dek + '</p>'
            '<div class="byline">By <strong>Propagation House</strong><span class="sep">·</span>' + byline + '</div></div>\n'
            '<div class="hero-figure"><div class="hero-img"><img src="../assets/images/' + hero_img + '" alt="' + hero_alt + '" /></div>'
            '<p class="caption">' + caption + '</p></div>\n'
            '<article class="article-body">\n' + body + '\n</article>\n'
            '<div class="article-foot"><div class="tags">' + tags + '</div>'
            '<div class="author-bio"><div class="avatar">P</div><div class="bio-text"><h4>Propagation House</h4>'
            '<div class="role">house Editorial</div>'
            '<p>Dispatches from the intelligence frontier. Propagation House tracks what the machines are becoming — and what it means for the people who build, fund, and regulate them.</p></div></div></div>\n'
            '<section class="related"><div class="section-label">Related Dispatches</div><div class="rel-grid">' + related + '</div></section>\n'
            + PROGRESS_JS + "\n</body>\n</html>\n")

# ============================================================
# ARTICLE 1 — SUPERMAN LEAPS (Unitree "Superman" reveal)
# ============================================================
body1 = """<p class="lead-para">The humanoid race spent this year arguing about hands, about balance, about whether a machine could fold a towel without tearing it. Unitree just changed the subject: it built a robot that can <em>jump two meters straight up</em> and sprint faster than any human alive, and it did it in just over three months.</p>
<p>On Monday the Hangzhou company previewed a new humanoid nicknamed "Superman" — a machine with 0.85-meter legs that cleared a standing vertical jump of two meters and hit a top speed of 12.66 meters per second, roughly 45 kilometers an hour. The company's claim is direct: both numbers exceed the best human records in the standing jump and the sprint. The robot did not simply improve on its predecessors. It moved the category from "walks like a person" to "performs like one" — and then kept going.</p>
<p>The timing is not incidental. Unitree unveiled the machine the same week it priced its Shanghai IPO, and days before the Second World Humanoid Robot Games open in Beijing's Ice Ribbon. The demonstration is a flex aimed at two audiences at once: the public market that just handed the company an 8,000x oversubscription, and the field of competitors about to line up on a running track in front of the world.</p>
<h2>Three Months Is <em>Not a Normal Timeline</em></h2>
<p>The detail that should stop anyone reading this is not the jump height. It is the development window. Unitree says Superman was developed in just over three months. For context, most humanoid programs treat a hardware revision as a multi-quarter project, and a gait breakthrough as a research milestone measured in years. A 2-meter vertical jump requires actuators with the power density of a small engine, a controller that can store and release energy through the leg like a spring, and a model that can time the whole sequence in milliseconds.</p>
<p>Doing that in a quarter suggests the bottleneck in humanoid robotics has shifted. The industry spent a decade convinced the hard part was the hardware — the joints, the batteries, the materials. Unitree's cadence implies the hard part is now <em>integration</em>: taking commodity actuators, a good model, and a manufacturing line that can iterate at software speed. When the constraint stops being physics and becomes process, the companies that can ship fastest will pull away from the ones still polishing a single perfect demo.</p>
<aside class="sidenote"><strong>Field Note</strong>The 12.66 m/s figure is roughly 45 km/h — faster than Usain Bolt's average speed in his 100m world record, which is the comparison Unitree's own materials reach for. The standing vertical jump of 2 meters exceeds the human record by a meaningful margin. Both numbers are company claims, and the honest read is that they are directionally true and precisely unverifiable — which is exactly how hardware marketing works in 2026.</aside>
<p>There is also a question of what "developed" means. A robot that jumps in a controlled demo is not the same as a robot that jumps reliably in a warehouse, a factory, or a construction site. The gap between a highlight reel and a deployment is where every humanoid company has historically come to grief. But the direction of travel matters more than the specific claim. The cost curve for athletic capability is collapsing, and it is collapsing fastest for the company that already has a public war chest and a national supply chain behind it.</p>
<div class="stat-row"><div class="stat"><div class="num">2<span class="unit">m</span></div><div class="label">Standing vertical jump — exceeds the human record, per Unitree</div></div><div class="stat"><div class="num">12.66<span class="unit">m/s</span></div><div class="label">Top sprint speed — about 45 km/h, faster than a human world-record pace</div></div><div class="stat"><div class="num">3<span class="unit">mo</span></div><div class="label">Development window — a hardware-and-gait cycle most labs would measure in years</div></div></div>
<h2>The Games Are the <em>Proof of Work</em></h2>
<p>The reveal lands directly ahead of the Second World Humanoid Robot Games, which open at the Ice Ribbon on August 22 with 51 events, 1,301 matches, and more than 2,000 robots from 16 countries. The competition is no longer a novelty showcase. It is becoming the humanoid equivalent of Formula One: a high-visibility arena where engineering claims get tested in public, under rules, in front of cameras and buyers.</p>
<p>That is why the "Superman" timing matters. A robot that can jump two meters is not a consumer product. It is a statement of physical capability aimed at the competitions, the procurement officers, and the investors who now have a ticker to watch. Unitree is not selling the jump. It is selling the fact that it can build something no one else has demonstrated, on a schedule no one else has matched, while the rest of the field is still walking.</p>
<blockquote class="offset-quote">Unitree is not selling the jump. It is selling the fact that it can build something no one else has demonstrated, on a schedule no one else has matched.<span class="attribution">- The cadence is the capability</span></blockquote>
<p>The uncomfortable question this raises for the rest of the industry is whether the athletic arms race is the right one. A robot that can sprint is impressive; a robot that can work a ten-hour shift without drifting is useful. The two are not the same engineering problem, and the capital chasing the highlight reel may be misallocated. But markets and games both reward spectacle, and Unitree has now demonstrated it can supply it on demand — while quietly keeping the balance sheet to fund the unglamorous work underneath.</p>
<div class="takeaways"><h4>What This Means</h4><ul><li><strong>The bottleneck has moved from hardware to process.</strong> A 2-meter jump developed in three months suggests the constraint is no longer actuator physics — it is how fast a company can integrate, iterate, and ship.</li><li><strong>The games are becoming a public proving ground.</strong> With 2,000+ robots from 16 countries competing at the Ice Ribbon, capability claims now get tested in front of buyers, not just cameras.</li><li><strong>Spectacle and utility are diverging.</strong> The athletic arms race is real, but the gap between a highlight-reel jump and a ten-hour work shift remains the place where value is actually created.</li></ul></div>
<p class="lead-para">The robot did not learn to walk this week. It learned to <em>fly</em> — two meters at a time, straight up, in front of a market that just decided to pay for the view.</p>"""

related1 = """<article><div class="kicker">Robotics</div><h3><a href="phantom-goes-public.html">The Phantom Goes Public</a></h3><div class="meta">8 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="beijing-games.html">The Games That Grade the Robots</a></h3><div class="meta">7 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="phantom-goes-to-europe.html">The Phantom Goes to Europe</a></h3><div class="meta">10 min read</div></article>"""

article1 = build(
    "Superman Leaps",
    "Robotics · Embodied AI",
    "Robotics · Embodied AI",
    "Superman <em>Leaps</em>",
    "Unitree's new humanoid jumps two meters straight up and sprints faster than any human alive — and the company says it built the whole thing in just over three months. The humanoid race just stopped arguing about hands and started arguing about <em>physics</em>.",
    "August 17, 2026<span class=\"sep\">·</span>8 min read",
    "superman-leaps-hero.jpg",
    "A humanoid robot frozen mid-leap in a dark arena, rendered as an archival darkroom print.",
    "The jump is the headline. The three-month development window is the story. When a robot's gait improves at software speed, the field's entire hierarchy has to be redrawn. <strong>Illustration by house.</strong>",
    body1,
    "<a href=\"#\">Unitree</a><a href=\"#\">Humanoid Robotics</a><a href=\"#\">Embodied AI</a><a href=\"#\">Athletics</a><a href=\"#\">China</a><a href=\"#\">Markets</a>",
    related1
)

# ============================================================
# ARTICLE 2 — BEIJING GAMES (World Humanoid Robot Games)
# ============================================================
body2 = """<p class="lead-para">Next Saturday, inside Beijing's National Speed Skating Oval — the Ice Ribbon, a building designed for the fastest humans on ice — more than two thousand robots will line up to run, kick, dance, clean, and fight fires. The Second World Humanoid Robot Games are not a trade show with a track meet attached. They are the moment the humanoid industry starts keeping <em>score</em>.</p>
<p>The numbers are staggering for a category that did not exist a decade ago: 51 events, 1,301 matches, 666 teams, and 2,056 robots from 16 countries, running August 22 through 26. The event list reads like an Olympic program grafted onto a factory audit — track and field, soccer, dance, housekeeping, firefighting, retail assistance. And unlike the first edition, many events now require the robots to operate <em>fully autonomously</em>, with limited or no remote control. The games have stopped being a demo reel and started being an exam.</p>
<p>That shift is the real news. A humanoid that can walk across a stage on a preprogrammed path is a toy. A humanoid that can navigate an unfamiliar course, make a decision, and complete a task without a human pulling strings is a product. The Beijing games are the first large-scale attempt to put that distinction on a scoreboard, in public, with prize money and procurement officers watching.</p>
<h2>From Exhibition to <em>Examination</em></h2>
<p>The inaugural games, held last year, were widely read as a spectacle — impressive, chaotic, and only loosely competitive. The 2026 edition has been designed to be taken seriously. The jump from 32 announced events to a final program of 51, and from a handful of teams to 666, signals an organizing committee that believes the format can carry real engineering weight. The autonomy rules are the tell: organizers have reportedly moved many events toward fully autonomous operation, which means the scores will separate the labs with genuine embodied intelligence from the ones with excellent teleoperation teams.</p>
<p>This is the humanoid equivalent of what happened to self-driving cars a decade ago, when the DARPA Grand Challenge separated the robotics labs that could actually navigate from the ones that could only demo. A public competition with hard rules and independent scoring compresses years of research into a single measurable outcome. For a field drowning in demo videos and marketing claims, that compression is overdue.</p>
<aside class="sidenote"><strong>Field Note</strong>The venue choice is deliberate. The Ice Ribbon was built for the 2022 Winter Olympics and is one of the most recognizable sporting landmarks in Beijing. Putting the humanoid games there is a statement that this is sport — and that China intends to host the definitive version of it.</aside>
<p>The range of events also maps directly onto the commercial case for humanoids. Housekeeping and retail assistance are the near-term deployment targets — the jobs where the economic math is closest to working. Firefighting and rescue are the aspirational market, where a robot's willingness to walk into a burning building justifies a price no warehouse operator would pay. Soccer and dance are the spectacle, the reason the games will be televised and the reason the category keeps its cultural momentum. The program is not random. It is a portfolio.</p>
<div class="stat-row"><div class="stat"><div class="num">2,056</div><div class="label">Robots from 16 countries — the largest humanoid competition ever staged</div></div><div class="stat"><div class="num">51</div><div class="label">Events and 1,301 matches across five days at the Ice Ribbon</div></div><div class="stat"><div class="num">666</div><div class="label">Teams — the field has grown from a showcase into an industry proving ground</div></div></div>
<h2>The Scoreboard Is the <em>Market Signal</em></h2>
<p>What happens in Beijing next week will be read as more than sport. With Unitree now a public company and the humanoid category newly priced on the Shanghai exchange, the games become a live feed of comparative capability — a way to see, in real time, which labs can actually deliver autonomy under pressure. The results will ripple into procurement decisions, funding rounds, and the balance sheets of the companies that can no longer hide behind carefully edited videos.</p>
<p>There is a geopolitical layer too. The games are being hosted by the country that has decided humanoid robotics is a strategic industry, at the same moment Washington is still debating whether to ban the leading Chinese maker's products. A competition where Chinese teams sweep the autonomy events will be used as evidence — fairly or not — that the center of gravity in embodied AI has moved. The scoreboard, in other words, is not just a scoreboard. It is a policy brief.</p>
<blockquote class="offset-quote">The games have stopped being a demo reel and started being an exam.<span class="attribution">- Autonomy is the subject</span></blockquote>
<p>The honest caveat is that a competition is still a controlled environment. Winning the housekeeping event at the Ice Ribbon is not the same as surviving a real hotel corridor at 3 a.m. with a drunk guest in the way. But the same was true of chess, and of Go, and of self-driving benchmarks. The pattern in AI is consistent: controlled tests get harder, edge cases get absorbed, and the gap between the exam and the job narrows faster than the skeptics predict. Beijing will not settle the humanoid race next week. It will just start keeping score — and the whole industry will have to look at the results.</p>
<div class="takeaways"><h4>What This Means</h4><ul><li><strong>Autonomy is now the exam.</strong> Many events require fully autonomous operation, which means scores will separate real embodied intelligence from teleoperation teams.</li><li><strong>The games are a market signal.</strong> With Unitree public and the category newly priced, results will ripple into procurement, funding, and policy.</li><li><strong>China is setting the venue and the rules.</strong> Hosting the definitive humanoid competition is a strategic choice, and the scoreboard will be read as a policy brief.</li></ul></div>
<p class="lead-para">The machines are not just walking anymore. They are lining up, in the building built for the fastest humans on earth, to find out who is fastest now.</p>"""

related2 = """<article><div class="kicker">Robotics</div><h3><a href="superman-leaps.html">Superman Leaps</a></h3><div class="meta">8 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="phantom-goes-public.html">The Phantom Goes Public</a></h3><div class="meta">8 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="gemini-robotics-2.html">The Body Electric</a></h3><div class="meta">9 min read</div></article>"""

article2 = build(
    "The Games That Grade the Robots",
    "Robotics · Competition",
    "Robotics · Competition",
    "The Games That <em>Grade</em> the Robots",
    "More than two thousand humanoids from sixteen countries will run, kick, clean, and fight fires at Beijing's Ice Ribbon next week — many of them fully autonomous, with no human pulling the strings. The humanoid industry is about to start keeping <em>score</em>.",
    "August 17, 2026<span class=\"sep\">·</span>7 min read",
    "beijing-games-hero.jpg",
    "Rows of humanoid robots on a running track inside a vast speed-skating oval, rendered as an archival darkroom print.",
    "The Ice Ribbon was built for the fastest humans on ice. Next week it hosts the largest field of humanoids ever assembled — and the first serious attempt to grade them in public. <strong>Illustration by house.</strong>",
    body2,
    "<a href=\"#\">World Humanoid Robot Games</a><a href=\"#\">Humanoid Robotics</a><a href=\"#\">Embodied AI</a><a href=\"#\">Autonomy</a><a href=\"#\">China</a><a href=\"#\">Competition</a>",
    related2
)

# ============================================================
# ARTICLE 3 — SAN MATEO PERMIT (first US humanoid regulation)
# ============================================================
body3 = """<p class="lead-para">While Beijing was getting ready to grade the robots, a county boardroom in California did something no other American jurisdiction has done: it voted to write the rules for who gets to deploy a <em>fleet</em> of humanoid robots — permits, kill switches, fire safety, and a requirement to track the jobs the machines displace. San Mateo County just became the first place in the United States to treat humanoids as something that needs a license.</p>
<p>On August 11 the Board of Supervisors unanimously adopted a resolution directing county staff to draft a comprehensive permitting process for commercial humanoid robots. The scope is specific and revealing: permits for deployment, emergency kill switches, fire safety measures, and — the provision that will make this ordinance a template for every other jurisdiction watching — tracking of job displacement. The county is not banning the robots. It is insisting that they be registered, supervised, and accounted for, the way a building or a restaurant is.</p>
<p>The significance is not the ordinance itself, which is still a draft. It is the category. For the first time in the United States, an elected body has decided that humanoid robots are not an exotic research topic but a foreseeable commercial reality that local government needs to regulate <em>in advance</em>. That is a shift in how the machine-adjacent future gets governed — from reaction to preparation.</p>
<h2>Why the First Mover Is a <em>County</em></h2>
<p>It is worth asking why San Mateo, of all places, moved first. The county sits at the northern edge of Silicon Valley, home to a dense concentration of the AI and robotics companies that will actually deploy these machines — and to the workers, unions, and civic groups that are already asking what happens when a robot takes a job. The resolution reads like a compromise negotiated in advance: industry gets a predictable path to deployment, labor gets visibility into displacement, and the county gets a kill switch it can point to when something goes wrong.</p>
<p>That triangular deal is likely to become the template. The federal government is nowhere on humanoid regulation — Washington is still arguing about whether to ban the leading Chinese maker's products at all. The states are moving piecemeal. That leaves counties and cities as the de facto rulemakers, and the jurisdictions with the most robots and the most political pressure are writing the rules first. San Mateo just showed the rest of them how.</p>
<aside class="sidenote"><strong>Field Note</strong>The resolution directs staff to draft the ordinance — it does not create the permit system yet. The timing matters: by the time the draft circulates, the Beijing games will have produced a public scoreboard of what these machines can actually do, and the drafters will have real capability data to regulate against.</aside>
<p>The specific provisions are worth reading as a checklist of what regulators fear. The kill switch requirement acknowledges that a robot in a public space is a physical safety device, not just a software process — and that remote control or emergency shutdown needs to be a design requirement, not an afterthought. The fire safety measures recognize that humanoids with lithium battery packs and motors are, in fire terms, more like e-bikes than like kiosks. And the job-displacement tracking is the provision with the longest shadow: it creates, for the first time, a public data stream on how many human jobs a robot fleet actually replaces.</p>
<div class="stat-row"><div class="stat"><div class="num">1<span class="unit">st</span></div><div class="label">US jurisdiction to vote for a humanoid fleet permitting framework</div></div><div class="stat"><div class="num">5<span class="unit">pts</span></div><div class="label">Permit, kill switch, fire safety, displacement tracking, and enforcement — the draft scope</div></div><div class="stat"><div class="num">11<span class="unit">Aug</span></div><div class="label">Date of the unanimous Board of Supervisors resolution</div></div></div>
<h2>The Permit Is the <em>New Product Launch</em></h2>
<p>For the robotics industry, this is a strategic event disguised as a bureaucratic one. Every humanoid company planning commercial deployment in the United States now has to ask a question its engineers never had to answer before: <em>where is your kill switch, and can you prove it works?</em> The companies that have been building safety into their platforms from the start will sail through a permitting regime. The ones that have been demoing first and asking questions later will find themselves grounded in the one county that matters most to their funding story.</p>
<p>There is also a subtle competitive dynamic. A predictable permitting regime is an advantage for incumbents with compliance teams and a moat against startups that cannot afford one. The first jurisdiction to write rules tends to export them: other counties and states will copy San Mateo's ordinance, the way they copy each other's building codes. The company that designs for San Mateo's requirements today is designing for the whole country tomorrow.</p>
<blockquote class="offset-quote">The county is not banning the robots. It is insisting that they be registered, supervised, and accounted for — the way a building or a restaurant is.<span class="attribution">- Governance catches up to the fleet</span></blockquote>
<p>The deeper read is that this is what maturity looks like. Every transformative technology eventually gets a permitting regime — buildings, cars, aircraft, biotech. The arrival of a county-level permit for humanoid fleets means the technology has crossed the threshold from novelty to infrastructure. It is no longer a question of whether the robots will be deployed. It is a question of who gets to deploy them, under what conditions, and with what accounting for the people whose jobs they change. San Mateo just wrote the first draft of that answer — and the rest of the country will be reading it.</p>
<div class="takeaways"><h4>What This Means</h4><ul><li><strong>Local government is becoming the de facto regulator.</strong> With Washington stalled and states moving piecemeal, counties like San Mateo are writing the rules that will become the template.</li><li><strong>The kill switch is now a design requirement.</strong> Any company planning US deployment must build shutdown, fire safety, and compliance into the platform — not bolt it on later.</li><li><strong>Job-displacement tracking creates a new data stream.</strong> For the first time, there will be public numbers on how many human jobs a robot fleet actually replaces — and that data will reshape the labor debate.</li></ul></div>
<p class="lead-para">The robots were never going to be stopped by a resolution. They were going to be <em>licensed</em> — and the county that wrote the first permit just became the most important regulator in American robotics.</p>"""

related3 = """<article><div class="kicker">Regulatory</div><h3><a href="act-takes-hold.html">The Act Takes Hold</a></h3><div class="meta">8 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="superman-leaps.html">Superman Leaps</a></h3><div class="meta">8 min read</div></article><article><div class="kicker">Robotics</div><h3><a href="phantom-goes-to-europe.html">The Phantom Goes to Europe</a></h3><div class="meta">10 min read</div></article>"""

article3 = build(
    "The Permit That Precedes the Fleet",
    "Regulatory · Robotics",
    "Regulatory · Robotics",
    "The Permit That <em>Precedes</em> the Fleet",
    "San Mateo County just became the first American jurisdiction to vote for a permitting framework for commercial humanoid robots — kill switches, fire safety, and job-displacement tracking included. The robots aren't banned. They're about to be <em>licensed</em>.",
    "August 17, 2026<span class=\"sep\">·</span>8 min read",
    "san-mateo-permit-hero.jpg",
    "A humanoid robot standing before a municipal government counter with a permitting form, rendered as an archival darkroom print.",
    "The permit counter is where the future actually gets decided. San Mateo's resolution is a draft — but it is the first draft of the rulebook the whole country will copy. <strong>Illustration by house.</strong>",
    body3,
    "<a href=\"#\">Regulation</a><a href=\"#\">Humanoid Robotics</a><a href=\"#\">San Mateo</a><a href=\"#\">Permitting</a><a href=\"#\">Labor</a><a href=\"#\">Safety</a>",
    related3
)

# ============================================================
# WRITE FILES
# ============================================================
out_dir = os.path.join(ROOT, "house-news", "articles")
files = {
    "superman-leaps.html": article1,
    "beijing-games.html": article2,
    "san-mateo-permit.html": article3,
}
for name, content in files.items():
    path = os.path.join(out_dir, name)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("WROTE", name, len(content), "chars")

# Sanity checks
for name in files:
    p = os.path.join(out_dir, name)
    with io.open(p, "r", encoding="utf-8") as f:
        t = f.read()
    assert t.count("<!DOCTYPE") == 1, name + " doctype"
    assert t.count("<head>") == 1, name + " head"
    assert t.count("<style>") == 1 and t.count("</style>") == 1, name + " style"
    assert t.count("<body>") == 1 and t.count("</body>") == 1, name + " body"
    assert "article-body" in t and "Propagation House" in t, name
    print("OK", name)
print("DONE")
