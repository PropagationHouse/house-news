# -*- coding: utf-8 -*-
"""Generate No. 89 heroes via Google Gemini image API (OpenRouter 402 fallback).

Same prompts as gen_images.py lane B; writes JPEGs straight into house-news assets.
"""
import base64, json, os, sys, urllib.request
from pathlib import Path

KEY = os.environ.get("GOOGLE_API_KEY", "")
OUT = Path(r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\house-news\assets\images")

LANE_B_HEAD = "Documentary photograph shot on 35mm Kodak Portra 400, "

JOBS = [
    ("anthropic-ipo-investor-day-hero.jpg",
     LANE_B_HEAD + "28mm f/4 prime, 1/60s: a closed-door investor briefing room set for a "
     "presentation in a San Francisco corporate headquarters, a long projection screen dark and "
     "blank at the front, neat rows of empty chairs facing it, a bound financial prospectus and a "
     "glass of water left on the lectern. Floor-to-ceiling windows half-shaded, cool morning "
     "daylight filtering through, a single downlight pooled on the lectern. Shot from the back row "
     "at seated height looking toward the screen, candid documentary distance, nobody in frame. "
     "The lectern, water glass and chair rows make the room scale obvious. Natural muted color, "
     "16:9 wide framing, no text, no signage, no logos, no people."),
    ("nvidia-china-share-hero.jpg",
     LANE_B_HEAD + "35mm f/2.8 prime, 1/60s: a distributor logistics warehouse staging aisle with "
     "pallets of plain antistatic cartons of accelerator hardware stacked and shrink-wrapped, one "
     "pallet half-emptied with a printed inventory tally sheet clipped to a board on top. Painted "
     "floor lanes and metal racking, high industrial ceiling lights with a pale patch of daylight "
     "from a loading door at the far end. Shot from the aisle at standing height looking down the "
     "row, candid documentary distance, nobody in frame. A hand pallet jack and floor scale beside "
     "the pallets make the carton stack scale obvious. Natural muted color, 16:9 wide framing, "
     "no text, no branding, no logos, no people."),
    ("exposed-ai-tooling-hero.jpg",
     LANE_B_HEAD + "35mm f/2.8 prime, 1/30s: an open network patch panel in a cramped office "
     "server closet with a bundle of ethernet cables running out through an unsecured door left "
     "ajar, several link lights blinking green on a switch below. Wire rack, power strips and a "
     "paper floor plan taped to the wall, bare overhead bulb plus green and amber switch LEDs "
     "glowing in the shadows. Shot close in from the doorway at chest height, candid documentary "
     "distance, nobody in frame. A coil of spare cable and a screwdriver on the rack shelf make "
     "the panel scale obvious. Natural muted color, 16:9 wide framing, no text, no logos, no people."),
]


def gen(name, prompt):
    dest = OUT / name
    if dest.exists() and dest.stat().st_size > 50000:
        print("SKIP exists", name)
        return True
    body = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE"], "imageConfig": {"aspectRatio": "16:9"}},
    }).encode()
    for model in ("gemini-3.1-flash-image", "gemini-2.5-flash-image"):
        url = "https://generativelanguage.googleapis.com/v1beta/models/" + model + ":generateContent"
        req = urllib.request.Request(url, data=body, method="POST", headers={
            "Content-Type": "application/json", "x-goog-api-key": KEY})
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.load(r)
        except Exception as e:
            print("ERR", model, name, repr(e)[:300])
            continue
        try:
            part = data["candidates"][0]["content"]["parts"][0]
            b64 = part.get("inlineData", {}).get("data")
            if not b64:
                print("NOIMG", model, json.dumps(data)[:400])
                continue
            dest.write_bytes(base64.b64decode(b64))
            print("OK", name, dest.stat().st_size, "bytes via", model)
            return True
        except Exception as e:
            print("PARSE", model, repr(e)[:300])
    return False


if __name__ == "__main__":
    ok = 0
    for n, p in JOBS:
        ok += bool(gen(n, p))
    print("DONE %d/%d" % (ok, len(JOBS)))
    sys.exit(0 if ok == len(JOBS) else 1)
