"""
Style Verification Batch v1 (Aug 26, 2026)
Purpose: prove the confirmed style system (STYLE_GUIDE.md) is repeatable
across the nuance of real articles. Every prompt is BUILT by
build_lane_a() / build_lane_b() from gen_images.py — slots filled,
skeleton kept verbatim. No hand-rolled prompt language.

Five real articles, chosen for lane-choice nuance:
  1. bolt-record-falls   -> B (hard-news scene, night stadium, motion)
  2. autonomy-majority   -> B (survey story, but lede gives a witnessable
                              place: the control room with the empty chair)
  3. alation-map-robbed  -> A (story is about the object itself — the
                              directory/map — presented as a studied thing)
  4. canvas-negotiate    -> B (soft feature, human scene, dusk studio)
  5. tsmc-capacity-wall  -> B (industrial, dwarfed-by-the-room anchor)
"""
import json, subprocess, base64, os, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gen_images import build_lane_a, build_lane_b

API_KEY = os.environ["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/images"
OUT = Path(__file__).parent / "assets" / "style-test-v1"
OUT.mkdir(parents=True, exist_ok=True)
MODEL = "black-forest-labs/flux.2-pro"

IMAGES = [
    {
        "filename": "test1-bolt-record-B.png",
        "label": "BOLT RECORD FALLS — Lane B (scene, night, motion)",
        "aspect_ratio": "16:9",
        "prompt": build_lane_b(
            subject="a humanoid robot sprinter caught mid-stride on an indoor stadium running track, body in sharp motion with faint motion blur at the ankles",
            place="a vast indoor athletics stadium at night, the empty bowl rising dark around the track",
            camera="from the opposite side of the track, wide framing",
            light="tall sodium floodlights through haze",
            scale_anchor="the robot is exactly human-sized, dwarfed by the stadium, the lane markers and track surface making the scale obvious",
        ),
    },
    {
        "filename": "test2-autonomy-majority-B.png",
        "label": "AUTONOMY MAJORITY — Lane B (survey story, witnessable place)",
        "aspect_ratio": "16:9",
        "prompt": build_lane_b(
            subject="an empty operator's chair in front of a row of dim monitoring consoles in a corporate control room",
            place="a real enterprise control room, rows of ordinary workstations and wall screens glowing faintly",
            camera="eye level, from the doorway, wide framing",
            light="flat fluorescent overhead light",
            scale_anchor="the chair is a normal office chair, the room full of ordinary desks and monitors, everything to true office scale",
        ),
    },
    {
        "filename": "test3-alation-map-A.png",
        "label": "ALATION MAP ROBBERY — Lane A (object itself is the news)",
        "aspect_ratio": "16:9",
        "prompt": build_lane_a(
            subject="a hand-drawn cartographer's map of an unnamed city, dense streets and small handwritten district labels, one district carefully outlined",
            detail="one outlined district",
        ),
    },
    {
        "filename": "test4-canvas-negotiate-B.png",
        "label": "CANVAS NEGOTIATES — Lane B (soft feature, human scene)",
        "aspect_ratio": "16:9",
        "prompt": build_lane_b(
            subject="a designer sitting at a desk in a small studio, working with a laptop and a large monitor showing a video-editing timeline",
            place="a small creative studio at dusk, posters and a whiteboard on the walls",
            camera="from across the room, candid distance",
            light="dusk window light mixed with the monitor's glow",
            scale_anchor="the person and desk are normal-sized, the studio room dwarfing them",
        ),
    },
    {
        "filename": "test5-tsmc-wall-B.png",
        "label": "TSMC CAPACITY WALL — Lane B (industrial, dwarfed by room)",
        "aspect_ratio": "16:9",
        "prompt": build_lane_b(
            subject="rows of sealed cleanroom bays and lithography machines stretching to the horizon of a semiconductor fab floor",
            place="an enormous semiconductor fabrication plant cleanroom, seen from a high catwalk",
            camera="wide framing from the catwalk, looking down the length of the floor",
            light="flat overcast cleanroom lighting",
            scale_anchor="tiny figures in pale bunny suits dwarfed by the machines and the room, the catwalk railing in the foreground making the scale obvious",
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

def contact_sheet(results, out_path):
    from PIL import Image, ImageDraw
    imgs = []
    for fn, label, path, _ in results:
        if path:
            im = Image.open(path).convert("RGB")
            im.thumbnail((1280, 720))
            imgs.append((label, im))
    if not imgs:
        print("no images for contact sheet")
        return
    W = 1280
    row_h = 720 + 44
    sheet = Image.new("RGB", (W, row_h * len(imgs) + 20), (24, 24, 22))
    d = ImageDraw.Draw(sheet)
    y = 10
    for label, im in imgs:
        d.text((10, y + 6), label, fill=(220, 210, 180))
        x = (W - im.width) // 2
        sheet.paste(im, (x, y + 40))
        y += row_h
    sheet.save(out_path, quality=88)
    print(f"contact sheet -> {out_path}")

if __name__ == "__main__":
    log = open(Path(__file__).parent / "style_test_v1.log", "a", encoding="utf-8")
    def logprint(*a):
        print(*a, flush=True)
        print(*a, file=log, flush=True)
    results = []
    for item in IMAGES:
        existing = OUT / item["filename"]
        if existing.exists() and existing.stat().st_size > 100000:
            logprint(f"SKIP {item['filename']} (exists)")
            results.append((item["filename"], item["label"], str(existing), existing.stat().st_size))
            continue
        logprint(f"Generating {item['filename']} ...")
        path, size = gen(item)
        results.append((item["filename"], item["label"], path, size))
        logprint(f"  -> {'OK' if path else 'FAILED'} ({size//1024} KB)")
        time.sleep(3)
    print("\nSUMMARY:")
    for fn, label, p, s in results:
        print(f"  {fn}: {'OK' if p else 'FAIL'}")
    checkin = Path(r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\image generations")
    checkin.mkdir(parents=True, exist_ok=True)
    for fn, label, p, s in results:
        if p:
            (checkin / fn).write_bytes(Path(p).read_bytes())
    contact_sheet(results, checkin / "style_test_v1.png")
    print("check-in copies ->", checkin)
