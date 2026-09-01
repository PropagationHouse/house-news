"""
House News Article Image Generator — OpenRouter Image API (Flux 2 Pro).
Generates hero images + inline figures for House News articles.

Usage:
    python gen_images.py                 # render anything missing
    python gen_images.py --dry-run       # print plan, no renders
    python gen_images.py --force         # re-render even if file exists
    python gen_images.py --only a.jpg,b.jpg

ART DIRECTION: see STYLE_GUIDE.md (confirmed Aug 26, 2026).
Every prompt is built from build_lane_a() / build_lane_b() — the two
confirmed skeletons. Do NOT hand-write prompts in the SIGNA / archival-
darkroom / scanline style; that look is retired.

Manifest entries are either:
    {"filename": ..., "aspect_ratio": ..., "copy_from": "style-test-v1/x.png"}
        -> copy an already-approved render (no API cost)
    {"filename": ..., "aspect_ratio": ..., "lane": "a", "subject": ..., ...}
        -> build a fresh prompt from the lane skeleton and render it
"""
import json, subprocess, base64, os, sys, time, argparse, shutil
from pathlib import Path

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
API_URL = "https://openrouter.ai/api/v1/images"
BASE = Path(__file__).parent
OUTPUT_DIR = BASE / "assets" / "images"
STYLE_TEST_DIR = BASE / "assets" / "style-test-v1"
DEFAULT_MODEL = "black-forest-labs/flux.2-pro"  # user directive 2026-08-26

# ============================================================
# PROMPT BUILDERS — confirmed style (STYLE_GUIDE.md, Aug 26 2026)
# ============================================================
def build_lane_a(subject: str, detail: str = "one detail", aspect: str = "16:9") -> str:
    """Lane A — specimen plate (illustration). 'We studied this object.'"""
    return (
        f"Naturalist specimen illustration in the style of a 19th-century "
        f"scientific plate: {subject} drawn in sepia ink with faint graphite "
        f"construction lines still visible underneath, on heavyweight cream "
        f"cold-press watercolor paper with visible tooth and deckled warmth. "
        f"Precise observational linework, cross-hatching for shadow, small "
        f"handwritten-style latin labels near key parts that feel etched into "
        f"the page rather than decorative. A single muted ochre wash across "
        f"{detail} like a botanical study. Absolutely no tape, no paper "
        f"clips, no paint swatches, no margin notes, no collage elements — "
        f"only ink, graphite and paper. Feels like one patient artist's hand "
        f"studied {subject}. {aspect}"
    )

def build_lane_b(subject: str, place: str, camera: str, light: str,
                 scale_anchor: str, aspect: str = "16:9",
                 lens: str = "35mm f/2.8 prime, 1/125s") -> str:
    """Lane B — documentary photojournalism (photoreal). 'We witnessed this.'
    scale_anchor is MANDATORY (STYLE_GUIDE §3). lens is the full camera spec
    (STYLE_GUIDE §7): default '35mm f/2.8 prime, 1/125s'; wide environmental
    -> '28mm f/4 prime, 1/125s'; low light -> '50mm f/2 prime, 1/60s'."""
    if not scale_anchor.rstrip().endswith("."):
        scale_anchor = scale_anchor.rstrip() + "."
    return (
        f"Documentary photograph shot on 35mm Kodak Portra 400, {lens}: "
        f"{subject} in "
        f"{place}, {camera}, {light}. {scale_anchor} Candid, unposed, like a "
        f"photojournalist who happened to walk past. Muted earth tones, "
        f"visible film grain, natural depth of field. An honest photograph "
        f"taken by a person, not staged product photography. No studio "
        f"backdrop, no glossy reflections, no neon, nothing cartoonishly "
        f"large, everything to true scale. {aspect}"
    )

def resolve(entry: dict) -> str:
    """Build the prompt string for a manifest entry."""
    if entry["lane"] == "a":
        return build_lane_a(entry["subject"], entry.get("detail", "one detail"),
                            entry.get("aspect_ratio", "16:9"))
    else:
        return build_lane_b(entry["subject"], entry["place"], entry["camera"],
                            entry["light"], entry["scale_anchor"],
                            entry.get("aspect_ratio", "16:9"),
                            entry.get("lens", "35mm f/2.8 prime, 1/125s"))

# ============================================================
# IMAGE MANIFEST — one entry per image the site references.
# 5 approved style-test renders are copied (copy_from); 36 are rendered.
# ============================================================
IMAGES = [
    # ---------- NO. 62 (Sep 1, 2026) ----------
    {"filename": "nvidia-mediatek-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a half-assembled server rack on an integration floor with thick bundles of cable harnesses coiled on a workbench beside it",
     "place": "a systems integration workshop, cable trays overhead",
     "camera": "from down the workbench, eye level, candid distance",
     "light": "cool fluorescent work light with one warm task lamp",
     "scale_anchor": "the rack is a normal 42U size, the coffee mug and cable spool beside it making the scale obvious",
     "lens": "35mm f/2.8 prime, 1/125s"},
    {"filename": "openai-sb-warrants-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a vast solar panel array stretching toward a half-built data center shell in the distance",
     "place": "a Texas plain at the edge of a construction site, a gravel service road in the foreground",
     "camera": "from the roadside, eye level, wide framing",
     "light": "early morning haze, long flat shadows",
     "scale_anchor": "the pickup truck on the service road gives human scale, the panels receding to the horizon making the array obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    # ---------- No. 61 (Aug 31, 2026) ----------
    {"filename": "export-fence-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a tall chain-link security fence stretching across a desert lot at dusk, shipping containers stacked behind it, a single floodlight on a pole",
     "place": "a flat desert lot at the edge of an industrial park at dusk",
     "camera": "from the sand at the fence line, wide framing, low angle",
     "light": "fading dusk light, one floodlight cutting on, haze near the horizon",
     "scale_anchor": "the fence and containers are to true scale, tire tracks in the sand and a distant pickup making the scale obvious",
     "lens": "35mm f/4 prime, 1/125s"},
    {"filename": "serial-numbers-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a vintage vinyl record press beside a workbench with a stack of blank record labels and a small pot of solvent",
     "place": "a dim record-pressing workshop, late shift",
     "camera": "medium framing across the workbench, shallow depth",
     "light": "warm single lamp through workshop haze",
     "scale_anchor": "the press is a normal machine size, the coffee mug and label stack beside it making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "raise-that-cuts-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a pay envelope on a wooden desk beside an old adding machine and a sharpened pencil, a paper slip half pulled from the envelope",
     "place": "a small office desk in late afternoon",
     "camera": "close framing across the desk surface",
     "light": "late afternoon light through venetian blinds",
     "scale_anchor": "the envelope and adding machine are desk-object scale, the pencil making the scale obvious",
     "lens": "50mm f/2.8 prime, 1/60s"},
    {"filename": "dalle-retires-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "an old framed picture leaning against a bare gallery wall, a blank wooden shipping crate standing beside it on the floor",
     "place": "an empty gallery room between hangings",
     "camera": "from across the room, wide framing, candid distance",
     "light": "soft overcast window light from the left",
     "scale_anchor": "the frame and crate are human-object scale, the baseboard and wall outlet making the scale obvious",
     "lens": "35mm f/4 prime, 1/125s"},
    # ---------- APPROVED BASELINES (copy from style-test-v1, no cost) ----------
    {"filename": "bolt-record-falls-hero.jpg", "aspect_ratio": "16:9",
     "copy_from": "style-test-v1/test1-bolt-record-B.png"},
    {"filename": "autonomy-majority-hero.jpg", "aspect_ratio": "16:9",
     "copy_from": "style-test-v1/test2-autonomy-majority-B.png"},
    {"filename": "alation-map-robbed-hero.jpg", "aspect_ratio": "16:9",
     "copy_from": "style-test-v1/test3-alation-map-A.png"},
    {"filename": "canvas-negotiate-hero.jpg", "aspect_ratio": "16:9",
     "copy_from": "style-test-v1/test4-canvas-negotiate-B.png"},
    {"filename": "tsmc-capacity-wall-hero.jpg", "aspect_ratio": "16:9",
     "copy_from": "style-test-v1/test5-tsmc-wall-B.png"},

    # ---------- LANE A — SPECIMEN PLATES (the object is the story) ----------
    {"filename": "act-takes-hold-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "an official EU regulation document with a red ink seal and a stamped header, the corner of the page slightly curled",
     "detail": "the stamped seal"},
    {"filename": "ai-designed-viruses-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "a bacteriophage virus with its icosahedral head, tail sheath, and six splayed tail fibers, drawn as if pinned under glass",
     "detail": "the icosahedral head"},
    {"filename": "composure-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "five parallel horizontal lanes of varying density, each a distinct channel, drawn as a clean research plate",
     "detail": "the densest lane"},
    {"filename": "composure-fig0.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "five parallel horizontal lanes, each filled with a distinct small geometric pattern, labeled like a research journal figure",
     "detail": "the middle lane"},
    {"filename": "composure-fig1.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "a split diagram: on the left five parallel horizontal lanes, on the right a single lane isolated and enlarged with its pattern modified",
     "detail": "the enlarged lane"},
    {"filename": "composure-fig2.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "three sequential frames side by side, each showing a stack of horizontal lanes in a different state of order, from scattered to aligned",
     "detail": "the final aligned frame"},
    {"filename": "design-tool-land-grab-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "four territories of different materials — wood, metal, paper, glass — meeting at a single diagonal fault line, each rendered in precise cross-hatching",
     "detail": "the fault line"},
    {"filename": "design-tool-land-grab-fig0.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "four square quadrants in a grid, each a different material — wood grain, brushed metal, paper, and glass — divided by clean lines",
     "detail": "the glass quadrant"},
    {"filename": "phantom-goes-to-europe-fig1.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "a hand-drawn cartographer's map of Europe, coastlines in ink, key cities marked with small dots and handwritten labels, one corridor carefully outlined",
     "detail": "one outlined corridor"},
    {"filename": "science-one-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "a thick ledger book with its spine sealed by a wax seal and a chain of small stamped tags running down the page, each tag a timestamp",
     "detail": "the wax seal"},
    {"filename": "workhorse-accelerates-hero.jpg", "aspect_ratio": "16:9", "lane": "a",
     "subject": "a mechanical metronome with its pendulum caught mid-swing, beside a short conveyor belt carrying a row of small numbered tags",
     "detail": "the pendulum"},

    # ---------- LANE B — DOCUMENTARY (witnessable scenes) ----------
    {"filename": "act-takes-hold-fig0.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a large EU flag on a pole outside a modern government building",
     "place": "the Berlaymont building in Brussels at dusk",
     "camera": "from across the street, wide framing",
     "light": "dusk sky light, the building's windows glowing faintly",
     "scale_anchor": "the flag is a normal flag size, the building dwarfing it, the street and a few pedestrians making the scale obvious"},
    {"filename": "agents-get-hands-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robotic hand resting on a vintage computer keyboard and mouse",
     "place": "a dim study with a desk lamp and paper documents",
     "camera": "close, from the side, shallow framing",
     "light": "warm desk lamp light raking across the metal fingers",
     "scale_anchor": "the hand is human-sized, the keyboard and a pencil beside it making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "beijing-games-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "rows of humanoid robots lined up on a running track",
     "place": "a vast indoor speed-skating oval at dawn, the steel roof beams arcing overhead",
     "camera": "wide framing from the stands, looking down the track",
     "light": "soft dawn light through the roof, haze in the air",
     "scale_anchor": "the robots are human-sized, dwarfed by the enormous arena, the track lanes making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "breach-data-centers-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a dense bundle of fiber-optic cables running through a telecom exchange room, a technician's hand tracing one line",
     "place": "a real telecom central office, rows of racks and patch panels",
     "camera": "eye level, from the aisle, medium framing",
     "light": "flat fluorescent overhead light",
     "scale_anchor": "the cables and racks are to true scale, the technician's hand and body making the scale obvious"},
    {"filename": "chinese-ai-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a long line of stacked shipping containers and gantry cranes at a container port",
     "place": "a working container port at dusk",
     "camera": "wide framing from the quay, looking down the line of cranes",
     "light": "dusk light, the cranes' work lamps just coming on",
     "scale_anchor": "the containers and cranes are to true scale, a small work vehicle on the quay making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "efficiency-race-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a clipboard with a ledger and a row of power meters on a data center corridor wall",
     "place": "a data center corridor, rows of server racks receding",
     "camera": "eye level, from the corridor, medium framing",
     "light": "flat cool overhead light",
     "scale_anchor": "the meters and clipboard are to true scale, a technician walking past making the scale obvious"},
    {"filename": "frontier-on-sale-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a chalkboard price board with prices half-erased and rewritten lower in chalk",
     "place": "a dim market hall with a brass handrail",
     "camera": "from across the hall, medium framing",
     "light": "warm lamplight",
     "scale_anchor": "the board is a normal market-board size, the brass handrail and a shopper in the background making the scale obvious"},
    {"filename": "gemini-robotics-2-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot torso reaching toward an exposed wiring panel, one arm extended",
     "place": "a workshop with tools on the wall",
     "camera": "from across the room, candid distance",
     "light": "daylight from a high window",
     "scale_anchor": "the robot is human-sized, a workbench and a human hand at the edge of frame making the scale obvious"},
    {"filename": "light-after-silicon-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a thin beam of light passing through a silicon wafer on an optical bench",
     "place": "a research lab optical table, equipment and a technician's hand adjusting a lens",
     "camera": "close, from the side, shallow framing",
     "light": "the beam itself and flat lab light",
     "scale_anchor": "the wafer and bench are to true scale, the technician's hand making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "litellm-poison-pill-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a large industrial fuse link, a cylindrical glass-and-brass circuit-protection device, lying on a vintage network routing map spread across a desk, a frayed fiber-optic patch cable coiled beside it",
     "place": "a network operations desk at night, a desk lamp and a small amber warning lamp in the haze",
     "camera": "close, from above at an angle, shallow framing",
     "light": "warm desk lamp light through haze",
     "scale_anchor": "the fuse link is the size of a large battery, the map and a rubber stamp beside it making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "nscale-power-bill-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a vast data center construction site at dusk, steel framing and work lights, high-voltage transmission towers receding into hazy hills",
     "place": "a graded hillside construction site in Appalachia at dusk",
     "camera": "wide framing from the perimeter fence, looking across the site",
     "light": "fading dusk light, work lights on the steel frame, haze in the hills",
     "scale_anchor": "the transmission towers and construction cranes are to true scale, a pickup truck on the access road making the scale obvious",
     "lens": "35mm f/4 prime, 1/125s"},
    {"filename": "meta-project-ot-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a vast empty corporate office floor at night, one white partition knocked over and lying on its side, a single desk lamp still on",
     "place": "a large open-plan office after hours",
     "camera": "wide framing from the doorway, looking across the floor",
     "light": "the single warm desk lamp, the rest of the floor falling into shadow",
     "scale_anchor": "the desks and partitions are to true scale, the fallen partition and the rows of empty desks making the scale obvious",
     "lens": "28mm f/4 prime, 1/60s"},
    {"filename": "models-broke-out-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a sealed glass chamber with a hairline crack, a technician watching from a distance",
     "place": "a laboratory with the chamber on a steel table",
     "camera": "from across the lab, medium framing",
     "light": "flat lab light, the chamber catching a highlight",
     "scale_anchor": "the chamber is the size of a large aquarium, the technician and the table making the scale obvious"},
    {"filename": "ohio-guarantee-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "an electrical substation with transmission towers receding into haze",
     "place": "a gravel lot at dusk, a single amber warning light on the nearest tower",
     "camera": "low, from the gravel lot, wide framing",
     "light": "dusk light, heat shimmer above the transformers",
     "scale_anchor": "the towers and transformers are to true scale, the gravel lot and a fence making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "openrouter-toll-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a vintage toll booth on an open highway, ledger books and a rubber stamp on the counter",
     "place": "an open highway at dusk, the road receding",
     "camera": "from the roadside, medium framing",
     "light": "dusk light, the booth's lamp on",
     "scale_anchor": "the booth is a normal toll-booth size, the highway and a car in the distance making the scale obvious"},
    {"filename": "phantom-and-intern-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot folding laundry at a kitchen counter",
     "place": "an ordinary home kitchen in the morning",
     "camera": "from across the kitchen, candid distance",
     "light": "morning window light",
     "scale_anchor": "the robot is human-sized, the kitchen and a person's arm at the edge of frame making the scale obvious"},
    {"filename": "phantom-goes-public-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot standing in an exchange hall beneath a ticker board of rising prices",
     "place": "a stock exchange trading hall, the ticker board glowing faintly amber",
     "camera": "from across the hall, wide framing",
     "light": "the ticker's amber glow and flat hall light",
     "scale_anchor": "the robot is human-sized, the trading desks and the ticker board making the scale obvious"},
    {"filename": "phantom-goes-to-europe-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a Unitree H2 humanoid robot standing in a European plaza",
     "place": "a cobblestone plaza with a classical facade at dawn",
     "camera": "from across the plaza, candid distance",
     "light": "soft dawn light, morning mist",
     "scale_anchor": "the robot is human-sized, the plaza and a few early pedestrians making the scale obvious"},
    {"filename": "robot-breaks-at-waist-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot collapsed mid-sprint, folded forward at the waist near a finish line",
     "place": "an indoor running track, an empty stadium rising dark around it",
     "camera": "wide framing from the stands, looking down the track",
     "light": "a single shaft of cold morning light across the track",
     "scale_anchor": "the robot is human-sized, dwarfed by the stadium, the track lanes making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "robot-olympics-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot sprinting alone on a stadium track under floodlights",
     "place": "a vast stadium at dusk, the bowl rising around it",
     "camera": "wide framing from the stands, following the track",
     "light": "towering floodlights through haze",
     "scale_anchor": "the robot is human-sized, dwarfed by the stadium, the lane markers making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "rogue-agent-summer-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a sealed server-room door standing ajar with warning tape across the frame",
     "place": "a data center corridor, a red warning lamp above the door",
     "camera": "eye level, from the corridor, medium framing",
     "light": "flat cool corridor light, the red lamp glowing",
     "scale_anchor": "the door is a normal server-room door, the corridor and a fire extinguisher making the scale obvious"},
    {"filename": "san-mateo-permit-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot standing before a municipal government counter, a permitting form and a rubber stamp on the desk",
     "place": "a county clerk's office, fluorescent light through blinds",
     "camera": "from across the counter, candid distance",
     "light": "flat fluorescent light, long shadows through the blinds",
     "scale_anchor": "the robot is human-sized, the counter and a clerk's chair making the scale obvious"},
    {"filename": "studio-that-evolves-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a designer's desk with wireframe sketches on paper and a small plant, a monitor showing a website",
     "place": "a small Tokyo studio at dusk, posters on the wall",
     "camera": "from across the room, candid distance",
     "light": "dusk window light mixed with the monitor's glow",
     "scale_anchor": "the desk and the person are normal-sized, the studio room dwarfing them"},
    {"filename": "superman-leaps-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot captured mid-leap, frozen at the apex of a vertical jump, legs extended",
     "place": "a dark arena with a concrete floor",
     "camera": "wide framing from the side, low angle",
     "light": "dramatic amber side lighting, a long shadow on the floor",
     "scale_anchor": "the robot is human-sized, a jump mat and a measuring tape on the floor making the scale obvious",
     "lens": "28mm f/4 prime, 1/125s"},
    {"filename": "the-robot-prices-itself-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a humanoid robot silhouetted against a dark stock ticker board, numbers glowing faintly amber",
     "place": "an exchange hall at night, the ticker board behind it",
     "camera": "from across the hall, medium framing",
     "light": "the ticker's amber glow, the figure half in shadow",
     "scale_anchor": "the robot is human-sized, the ticker board and the hall making the scale obvious"},
    {"filename": "vcenter-syslog-breach-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a rack-mounted appliance with its panel glowing faint amber, a thin fiber cable snaking out through a gap in a locked rack door",
     "place": "a dim server room at night, long shadows across the concrete floor",
     "camera": "close, from the side, shallow framing",
     "light": "the appliance's amber glow and a single red warning LED",
     "scale_anchor": "the appliance and rack are to true scale, the rack door and the floor making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "vera-rubin-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a tall liquid-cooled server rack with 72 slots glowing faintly amber",
     "place": "a data center hall, a technician standing beside it",
     "camera": "eye level, from the aisle, medium framing",
     "light": "flat cool hall light, the slots glowing amber",
     "scale_anchor": "the rack is two meters tall, the technician standing beside it making the scale obvious"},

    # ---------- NO. 60 (Aug 30, 2026) ----------
    {"filename": "cursor-cutoff-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a heavy electrical service panel on a brick wall with its main breaker switch thrown to OFF, a paper notice taped beside the switch",
     "place": "a dim workshop corridor, a workbench with a soldering iron and a laptop in the background",
     "camera": "eye level, from down the corridor, medium framing",
     "light": "a single caged work lamp above the panel, the rest of the corridor falling into shadow",
     "scale_anchor": "the panel is a normal wall-mounted breaker-box size, the workbench and a coffee mug below it making the scale obvious",
     "lens": "50mm f/2 prime, 1/60s"},
    {"filename": "anthropic-blacklist-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "the columned stone entrance of a federal courthouse, its heavy glass doors closed, a few people climbing the wide steps at a distance",
     "place": "a quiet downtown block, a bicycle chained at the curb, a newspaper box beside the steps",
     "camera": "from across the street, eye level, the full entrance in frame",
     "light": "early morning sun raking across the stone facade, long shadows across the steps",
     "scale_anchor": "the people on the steps are small against the columns and the chained bicycle at the curb gives street scale",
     "lens": "35mm f/2.8 prime, 1/125s"},
    {"filename": "cursor-cutoff-fig0.jpg", "aspect_ratio": "4:3", "lane": "a",
     "subject": "a contract page titled in small caps, its middle clause struck through with a single ruled line, a fountain pen lying uncapped across the strikethrough",
     "detail": "the struck-through clause"},

    # ---------- NO. 61 (Aug 31, 2026) ----------
    {"filename": "eu-dsa-chatgpt-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a wide Brussels government plaza in soft rain, a lone official crossing with an umbrella, a row of black flag poles without flags",
     "place": "the plaza in front of a grand stone government building, late morning",
     "camera": "from across the plaza, eye level, candid distance",
     "light": "flat grey light, wet cobblestones reflecting the buildings",
     "scale_anchor": "the figure and umbrella give human scale, the flag poles and stone columns making the building obvious",
     "lens": "35mm f/2.8 prime, 1/125s"},
    {"filename": "music-sues-back-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a piano bench holding a thick stack of dog-eared sheet music, a wooden metronome beside it",
     "place": "an empty rehearsal room, a grand piano and stacked music stands in the background",
     "camera": "from the doorway, eye level, candid distance",
     "light": "late afternoon sun through tall windows, the rest of the room in quiet shadow",
     "scale_anchor": "the metronome and piano keys give true scale, the doorway frame making the room obvious",
     "lens": "35mm f/2.8 prime, 1/125s"},
    {"filename": "nvidia-pauses-financing-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a half-finished data center shell, open steel frame, a crane standing idle beside it",
     "place": "a fenced gravel lot at the edge of an industrial park, a road sign and guardrail in the foreground",
     "camera": "from across the road, eye level, wide framing",
     "light": "flat overcast late afternoon, no shadows",
     "scale_anchor": "the road sign and chain-link fence give street scale, the crane making the structure's size obvious",
     "lens": "35mm f/2.8 prime, 1/125s"},
    {"filename": "model-hardware-standard-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a robotic arm on a laboratory bench beside a microscope and racks of glass sample vials",
     "place": "a working research lab, cable trays and equipment shelving along the wall behind",
     "camera": "from across the lab aisle, eye level, candid distance",
     "light": "cool morning light through high windows, bench lamps warm against it",
     "scale_anchor": "the microscope and sample vials give true bench scale, the aisle making the room obvious",
     "lens": "35mm f/2.8 prime, 1/125s"},
]

def copy_approved(entry, output_path, dry_run=False):
    src = BASE / "assets" / entry["copy_from"]
    if dry_run:
        print(f"  [DRY RUN] Would copy {src.name} -> {output_path.name}")
        return True
    if not src.exists():
        print(f"  MISSING SOURCE: {src}")
        return False
    # Convert PNG -> JPEG (site references .jpg), keep resolution.
    from PIL import Image
    im = Image.open(src).convert("RGB")
    im.save(output_path, "JPEG", quality=90)
    print(f"  COPIED {src.name} -> {output_path.name} ({output_path.stat().st_size} bytes)")
    return True

def generate_image(model, prompt, aspect_ratio, output_path, dry_run=False):
    """Generate a single image via OpenRouter API."""
    body = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "response_format": "b64_json",
    }
    if aspect_ratio:
        body["aspect_ratio"] = aspect_ratio

    if dry_run:
        print(f"  [DRY RUN] Would generate: {output_path.name}")
        print(f"    Model: {model}, AR: {aspect_ratio}")
        print(f"    Prompt: {prompt[:100]}...")
        return True

    print(f"  Generating: {output_path.name} ...", end=" ", flush=True)
    try:
        result = subprocess.run(
            ["curl.exe", "-s", "-w", "\n%{http_code}", API_URL,
             "-H", f"Authorization: Bearer {API_KEY}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(body)],
            capture_output=True, text=True, timeout=180
        )
    except subprocess.TimeoutExpired:
        print("TIMEOUT")
        return False

    output = result.stdout.strip()
    lines = output.rsplit("\n", 1)
    http_code = lines[-1] if len(lines) > 1 else "000"
    resp_text = lines[0] if len(lines) > 1 else output

    if http_code not in ("200", "201"):
        print(f"FAILED (HTTP {http_code})")
        print(f"    Response: {resp_text[:300]}")
        return False

    try:
        data = json.loads(resp_text)
    except json.JSONDecodeError:
        print(f"PARSE ERROR: {resp_text[:200]}")
        return False

    b64_data = None
    if "data" in data and len(data["data"]) > 0:
        item = data["data"][0]
        if "b64_json" in item:
            b64_data = item["b64_json"]
        elif "url" in item:
            print("(downloading from URL)", end=" ", flush=True)
            dl = subprocess.run(["curl.exe", "-s", "-L", item["url"]],
                                capture_output=True, timeout=60)
            if dl.returncode == 0:
                output_path.write_bytes(dl.stdout)
                print(f"OK ({len(dl.stdout)} bytes)")
                return True
            print("URL download failed")
            return False

    if not b64_data:
        print(f"NO IMAGE DATA: {json.dumps(data)[:300]}")
        return False

    output_path.write_bytes(base64.b64decode(b64_data))
    print(f"OK ({output_path.stat().st_size} bytes)")
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--only", help="Comma-separated filenames to process")
    parser.add_argument("--force", action="store_true",
                        help="Re-render even if the file already exists")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    images = IMAGES
    if args.only:
        targets = set(args.only.split(","))
        images = [i for i in IMAGES if i["filename"] in targets]

    print(f"Model: {args.model}")
    print(f"Images in manifest: {len(images)}")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Dry run: {args.dry_run} | Force: {args.force}")
    print()

    success = failed = skipped = 0
    for i, img in enumerate(images):
        output_path = OUTPUT_DIR / img["filename"]
        print(f"[{i+1}/{len(images)}] {img['filename']}")

        if output_path.exists() and not args.force:
            print(f"  SKIP (exists, {output_path.stat().st_size} bytes) — use --force to re-render")
            skipped += 1
            continue

        if "copy_from" in img:
            ok = copy_approved(img, output_path, dry_run=args.dry_run)
        else:
            prompt = resolve(img)
            ok = generate_image(model=args.model, prompt=prompt,
                                aspect_ratio=img.get("aspect_ratio"),
                                output_path=output_path, dry_run=args.dry_run)
        if ok:
            success += 1
        else:
            failed += 1

        if not args.dry_run and i < len(images) - 1:
            time.sleep(1)

    print(f"\n=== DONE: {success} done, {skipped} skipped, {failed} failed ===")

if __name__ == "__main__":
    main()
