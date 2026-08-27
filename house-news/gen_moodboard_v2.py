"""
Moodboard Batch 3 (v2) — corrections from v1 review.
Rule 1 (Lane B): documentary photojournalism. Real place, camera distance,
available light, lived-with objects. NO cute characters, NO studio staging.
Rule 2 (Lane A): material honesty only. NO scrapbook props (tape/swatches/
annotations). The hand shows in line pressure and substrate, not decoration.
"""
import json, subprocess, base64, os, sys, time
from pathlib import Path

API_KEY = os.environ["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/images"
OUT = Path(__file__).parent / "assets" / "moodboard-v2"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "google/gemini-3.1-flash-image"

IMAGES = [
    {
        "filename": "B-sidewalk-fieldtest.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph shot on 35mm Kodak Portra 400: a humanoid "
            "robot being field-tested on an ordinary city sidewalk beside a bus "
            "stop, late afternoon under flat overcast light. Camera positioned "
            "across the street at eye level, candid distance, like a "
            "photojournalist who happened to walk past — the robot is mid-task, "
            "a technician crouched nearby with a laptop case, unposed. Muted "
            "earth tones, soft grey sky, brick and concrete textures, subtle "
            "film grain and natural Portra warmth. Completely ordinary scene, "
            "no drama, no rim lighting, no cinematic mood, no neon. Looks like "
            "a real press photograph from a news wire service."
        ),
    },
    {
        "filename": "B-gripper-newspaper.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary still-life photograph on 35mm Kodak Portra 400: a worn "
            "industrial robot gripper hand resting on a folded broadsheet "
            "newspaper on a scarred wooden workbench covered in fine dust and "
            "scratches. Morning window light from the left, soft falloff, faint "
            "dust motes. The gripper is clearly used — scuffed paint, worn "
            "finger pads, a cable zip-tied along the wrist. Warm muted earth "
            "tones, visible film grain, shallow depth of field. Reads as an "
            "honest workshop photograph taken by a person, not staged product "
            "photography. No studio backdrop, no glossy reflections, no neon."
        ),
    },
    {
        "filename": "A-specimen-plate.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Naturalist specimen illustration in the style of a 19th-century "
            "scientific plate: a humanoid robot arm drawn in sepia ink with "
            "faint graphite construction lines still visible underneath, on "
            "heavyweight cream cold-press watercolor paper with visible tooth "
            "and deckled warmth. Precise observational linework, cross-hatching "
            "for shadow, small handwritten-style latin labels near joints that "
            "feel etched into the page rather than decorative. A single muted "
            "ochre wash across one joint like a botanical study. Absolutely no "
            "tape, no paper clips, no paint swatches, no margin notes, no "
            "collage elements — only ink, graphite and paper. Feels like one "
            "patient artist's hand studied the machine."
        ),
    },
    {
        "filename": "A-dark-paper-roots.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Ink illustration on heavyweight black cotton rag paper: fiber-optic "
            "cables that split and taper into living root systems, drawn in warm "
            "white and cream ink with fine parallel hatching, the roots ending "
            "in delicate hair-roots rendered in thin confident strokes. Visible "
            "paper texture through the ink, slight natural ink bleed where lines "
            "meet, one restrained copper-toned accent where cable becomes root. "
            "Composition calm and centered like a botanical plate. No glow "
            "effects, no neon, no gradient lighting, no collage props — only "
            "ink on dark textured paper, one consistent hand."
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

if __name__ == "__main__":
    results = []
    for item in IMAGES:
        print(f"Generating {item['filename']} ...")
        path, size = gen(item)
        results.append((item["filename"], path, size))
        print(f"  -> {'OK' if path else 'FAILED'} ({size//1024} KB)")
        time.sleep(3)
    print("\nSUMMARY:")
    for fn, p, s in results:
        print(f"  {fn}: {'OK' if p else 'FAIL'}")
