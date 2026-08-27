"""
Moodboard Batch 4 (v3) — gripper scale fix only.
v2 verdict: Lane A confirmed (specimen plate). B-sidewalk fine.
B-gripper reads as Open Claw (subject works) but "feels off":
nothing should look cartoonishly large or out of place.

Fix: every prompt now pins real-world scale — the gripper is a
normal-sized industrial part (hand-sized), with in-frame scale
anchors (mug, pencil, human hand, workshop context). No hero
cropping that inflates the subject.
"""
import json, subprocess, base64, os, sys, time
from pathlib import Path

API_KEY = os.environ["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/images"
OUT = Path(__file__).parent / "assets" / "moodboard-v3"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "black-forest-labs/flux.2-pro"  # user default, 2026-08-26

IMAGES = [
    {
        "filename": "B-gripper-mug-scale.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary still-life photograph shot on 35mm Kodak Portra 400: a "
            "normal-sized worn industrial robot gripper, roughly the size of a "
            "human hand, resting on a folded broadsheet newspaper on a scarred "
            "wooden workbench. Next to it, an ordinary coffee mug and a pencil "
            "make the scale obvious — the gripper is small, hand-sized, not "
            "oversized. Morning window light from the left, soft falloff, faint "
            "dust motes, fine dust and scratches on the bench. Scuffed paint, "
            "worn finger pads, a cable zip-tied along the wrist. Warm muted "
            "earth tones, visible film grain, natural depth of field. An honest "
            "workshop photograph taken by a person, not staged product "
            "photography. No studio backdrop, no glossy reflections, no neon, "
            "nothing cartoonishly large, everything to true scale."
        ),
    },
    {
        "filename": "B-gripper-human-hand.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph shot on 35mm Kodak Portra 400: a technician's "
            "weathered hand and forearm entering the frame from the right, "
            "holding a normal-sized industrial robot gripper — the gripper is "
            "clearly the same size as the hand, a small hand-sized device, "
            "examining it over a folded newspaper on a workbench. The human "
            "hand is the scale reference and is prominent. Late afternoon "
            "window light, flat and soft, workshop background softly out of "
            "focus with shelves and tools. Muted earth tones, visible film "
            "grain, candid and unposed, like a photojournalist's frame. No "
            "drama, no rim lighting, no neon, nothing cartoonishly large, "
            "everything to true human scale."
        ),
    },
    {
        "filename": "B-gripper-press-context.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph shot on 35mm Kodak Portra 400: a real "
            "industrial press in a working machine shop, its small end-of-arm "
            "gripper (hand-sized, normal scale) holding a folded broadsheet "
            "newspaper at the end of a long steel arm. The machine fills the "
            "frame so the gripper reads as one small part of a large ordinary "
            "machine, not a hero object. A technician's jacket hangs on a hook "
            "in the background, a workbench with a mug and tools nearby. "
            "Overcast light through a high window, flat and honest. Muted "
            "earth tones, visible film grain, candid distance like a news wire "
            "photo. No studio staging, no glossy reflections, no neon, nothing "
            "cartoonishly large, everything to true scale."
        ),
    },
    {
        "filename": "B-gripper-bench-wide.png",
        "aspect_ratio": "16:9",
        "prompt": (
            "Documentary photograph shot on 35mm Kodak Portra 400, wide framing: "
            "a cluttered real workshop bench seen from across the room — a "
            "small normal-sized industrial robot gripper sitting among ordinary "
            "objects: a coffee mug, a pencil, a pair of pliers, a folded "
            "broadsheet newspaper, a tape measure. The gripper is just one "
            "small item among many, clearly hand-sized, dwarfed by the bench. "
            "Flat overcast morning light, no hero lighting, nothing isolated or "
            "glowing. Muted earth tones, visible film grain, the honest "
            "messiness of a real workbench. No studio backdrop, no neon, "
            "nothing cartoonishly large, everything to true scale."
        ),
    },
]

def gen(item):
    payload = {
        "model": MODEL,
        "prompt": item["prompt"],
        "n": 1,
        "response_format": "b64_json",
        "aspect_ratio": item["aspect_ratio"],
    }
    for attempt in range(3):
        try:
            r = subprocess.run(
                ["curl.exe", "-s", "-w", "\n%{http_code}", API_URL,
                 "-H", f"Authorization: Bearer {API_KEY}",
                 "-H", "Content-Type: application/json",
                 "-d", json.dumps(payload)],
                capture_output=True, text=True, timeout=180)
            out = r.stdout
            lines = out.rsplit("\n", 1)
            body = lines[0] if len(lines) == 2 else out
            code = lines[1].strip() if len(lines) == 2 else "?"
            data = json.loads(body)
            if "data" in data and data["data"] and "b64_json" in data["data"][0]:
                img = base64.b64decode(data["data"][0]["b64_json"])
                path = OUT / item["filename"]
                path.write_bytes(img)
                return str(path), len(img)
            print(f"  attempt {attempt+1} bad response (http {code}): {body[:300]}")
        except Exception as e:
            print(f"  attempt {attempt+1} error: {e}")
        time.sleep(5)
    return None, 0

if __name__ == "__main__":
    results = []
    for item in IMAGES:
        print(f"Generating {item['filename']} ...", flush=True)
        path, size = gen(item)
        results.append((item["filename"], path, size))
        print(f"  -> {'OK' if path else 'FAILED'} ({size//1024} KB)", flush=True)
        time.sleep(3)
    print("\nSUMMARY:")
    for fn, p, s in results:
        print(f"  {fn}: {'OK' if p else 'FAIL'}")
