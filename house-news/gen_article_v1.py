"""
Article image pass v1 - four REAL articles, bespoke art direction each.
Lane B rules: documentary photojournalism, real place, candid distance,
available light, Portra 400. Ordinary beats cinematic. Always.
Lane A rules: material honesty only. Textured heavyweight paper, ink+graphite,
no props/tape/swatches/collage. One patient hand. Absence/composition carries meaning.
No readable text in ANY prompt (models garble it).
"""
import json, subprocess, base64, os, sys, time
from pathlib import Path

API_KEY = os.environ["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/images"
OUT = Path(__file__).parent / "assets" / "article-v1"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "google/gemini-3.1-flash-image"

IMAGES = [
    {
        # ARTICLE: robot-olympics.html - "The Robot Olympics Open"
        # Story: Beijing convened 2,056 robots / 666 teams / 16 countries.
        # Angle: NOT the spectacle - the mundane backstage reality. Wire-photo logic.
        "filename": "olympics-backstage-corridor.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph shot on 35mm Kodak Portra 400: a plain "
            "concrete service corridor beneath a large sports arena in Beijing "
            "between event sessions. Two humanoid robots stand parked against "
            "the wall, switched off or idling, one power cable coiled loose on "
            "the floor beside a stack of plastic water bottles and a metal "
            "folding chair. A tired technician sits on the chair checking a "
            "phone, seen from behind at mid distance. Flat fluorescent light "
            "mixed with grey daylight from an open door far down the corridor. "
            "Camera at eye level, candid, unposed, like a photojournalist "
            "walking between venues who paused for one frame. Scuffed concrete, "
            "cable trays, muted earth tones, subtle film grain. An ordinary "
            "backstage moment, no drama, no rim lighting, no neon, no readable "
            "signage. Looks like a real press photograph from a news wire service."
        ),
    },
    {
        # ARTICLE: frontier-on-sale.html - "The Frontier Goes on Sale"
        # Story: OpenAI cuts GPT-5.6 Sol API pricing ~33%, 'promotional'.
        # Angle: compute as anonymous commodity. Business-section wire photo.
        # Object/scene, zero people, zero logos, zero legible text.
        "filename": "frontier-commodity-dock.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph on 35mm Kodak Portra 400: a loading dock "
            "at dawn outside a plain distribution warehouse. Wooden pallets "
            "stacked with identical unbranded cardboard boxes wrapped in clear "
            "plastic, a hand truck leaning against the concrete wall, damp "
            "asphalt reflecting a flat overcast sky. Nothing labeled, nothing "
            "branded - pure anonymous commodity waiting to move. Camera low "
            "near the dock edge, calm wide framing, soft grey morning light, "
            "muted earth tones of cardboard and wet concrete, fine film grain. "
            "Reads like a wire-service business-section photograph about supply "
            "and price. Honest, unstaged, no people, no dramatic sky, no neon, "
            "no cinematic contrast, no readable text anywhere."
        ),
    },
    {
        # ARTICLE: alation-map-robbed.html - "The Map of Everything Gets Robbed"
        # Story: breach at THE data catalog - the enterprise's map of its own
        # data stolen. Lane A, DARK PAPER variant (white ink on black rag).
        # Meaning carried by absence: unfinished regions where ink stops.
        "filename": "alation-map-absence.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Ink illustration on heavyweight black cotton rag paper: a "
            "cartographer's plan of an imagined great archive drawn entirely "
            "in warm white and cream ink - rooms, shelving ranges, index "
            "corridors and tiny catalog drawers rendered as fine parallel "
            "hatching like an old atlas plate. Several whole districts of the "
            "map are simply unfinished: bare black paper where the linework "
            "stops mid-stroke, edges trailing off into nothing, as if entire "
            "regions were lifted away. The absence is the subject. Visible "
            "paper texture through the ink, slight natural ink bleed, one "
            "single thin copper-toned line tracing a path through the surviving "
            "half of the map. Calm centered composition, no glow effects, no "
            "neon, no collage, no torn-paper props, no readable words - only "
            "white ink on dark textured paper, one patient hand."
        ),
    },
    {
        # ARTICLE: canvas-negotiate.html - "The Canvas Learns to Negotiate"
        # Story: agentic co-creation canvases - human and agent sharing the
        # same surface, tooling negotiating over the work. Lane A, CREAM
        # cold-press variant. Negotiation told through line pressure change.
        "filename": "canvas-two-hands-one-line.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Observational ink and graphite illustration on heavyweight cream "
            "cold-press watercolor paper: a worn wooden drafting table seen "
            "from directly above, drawn like a 19th-century naturalist "
            "specimen plate - a steel ruler, a drafting compass, a worn "
            "eraser, and a sheet of drawing paper bearing one long confident "
            "line that crosses the sheet; partway along, the line changes "
            "character - different pressure, slightly different weight - and "
            "continues to the far edge as if a second hand took over "
            "mid-stroke without stopping. Sepia ink over faint graphite "
            "construction lines, cross-hatched shadows beneath the tools, one "
            "restrained ochre wash blooming exactly where the two line "
            "characters meet. Visible paper tooth, natural ink bleed. "
            "Absolutely no tape, no paint swatches, no margin notes, no "
            "collage elements, no readable text - only ink, graphite and "
            "paper, one consistent patient hand studying the act of drawing."
        ),
    },
]

def gen(item):
    payload = {
        "model": MODEL,
        "prompt": item["prompt"],
        "aspect_ratio": item["aspect_ratio"],
    }
    for attempt in range(3):
        try:
            r = subprocess.run(
                ["curl", "-s", API_URL,
                 "-H", f"Authorization: Bearer {API_KEY}",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=180)
            data = json.loads(r.stdout)
            if "data" in data and data["data"] and "b64_json" in data["data"][0]:
                img = base64.b64decode(data["data"][0]["b64_json"])
                path = OUT / item["filename"]
                path.write_bytes(img)
                return str(path), len(img)
            print(f"  attempt {attempt+1} bad response: {r.stdout[:300]}")
        except Exception as e:
            print(f"  attempt {attempt+1} error: {e}")
        time.sleep(5)
    return None, 0

def contact_sheet(paths, out_path):
    try:
        from PIL import Image, ImageDraw
        cols, rows, cell_w, cell_h, pad = 2, 2, 800, 450, 20
        sheet = Image.new("RGB", (cols*cell_w + pad*(cols+1),
                                  rows*cell_h + pad*(rows+1)), (24, 22, 20))
        draw = ImageDraw.Draw(sheet)
        for i, p in enumerate(paths):
            if not p:
                continue
            im = Image.open(p).convert("RGB")
            im.thumbnail((cell_w, cell_h))
            x = pad + (i % cols) * (cell_w + pad)
            y = pad + (i // cols) * (cell_h + pad)
            sheet.paste(im, (x, y))
        sheet.save(out_path)
        return out_path
    except Exception as e:
        print(f"sheet failed: {e}")
        return None

if __name__ == "__main__":
    results = []
    for item in IMAGES:
        print(f"Generating {item['filename']} ...")
        path, size = gen(item)
        results.append((item["filename"], path, size))
        print(f"  -> {'OK' if path else 'FAILED'} ({size//1024} KB)")
        time.sleep(3)
    print("\nSUMMARY:")
    ok_paths = []
    for fn, p, s in results:
        print(f"  {fn}: {'OK' if p else 'FAIL'}")
        if p:
            ok_paths.append(p)
    if len(ok_paths) >= 2:
        sheet = contact_sheet(ok_paths, r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp\article_v1_sheet.png")
        print(f"SHEET: {sheet}")
