# -*- coding: utf-8 -*-
"""Add No. 89 (Oct 14, 2026) hero manifest entries to gen_images.py."""
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "house-news" / "gen_images.py"
s = P.read_text(encoding="utf-8")

NEW = '''IMAGES = [
    # ---------- NO. 89 (Oct 14, 2026) ----------
    {"filename": "anthropic-ipo-investor-day-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a closed-door investor briefing room set for a presentation, a long projection screen dark and blank at the front, neat rows of empty chairs facing it, a bound financial prospectus and a glass of water left on the lectern",
     "place": "a corporate headquarters briefing room in San Francisco with floor-to-ceiling windows half-shaded",
     "camera": "from the back row at seated height looking toward the screen, candid documentary distance, nobody in frame",
     "light": "cool morning daylight filtering through the half-shaded windows, a single downlight pooled on the lectern",
     "scale_anchor": "the lectern, water glass and chair rows make the room scale obvious.",
     "lens": "28mm f/4 prime, 1/60s"},
    {"filename": "nvidia-china-share-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a warehouse staging aisle with pallets of plain antistatic cartons of accelerator hardware stacked and shrink-wrapped, one pallet half-emptied with a printed inventory tally sheet clipped to a board on top",
     "place": "a distributor logistics warehouse with painted floor lanes and metal racking",
     "camera": "from the aisle at standing height looking down the row, candid documentary distance, nobody in frame",
     "light": "high industrial ceiling lights with a pale patch of daylight from a loading door at the far end",
     "scale_anchor": "a hand pallet jack and floor scale beside the pallets make the carton stack scale obvious.",
     "lens": "35mm f/2.8 prime, 1/60s"},
    {"filename": "exposed-ai-tooling-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "an open network patch panel in a small server closet with a bundle of ethernet cables running out through an unsecured door left ajar, several link lights blinking green on a switch below",
     "place": "a cramped office server closet with a wire rack, power strips and a paper floor plan taped to the wall",
     "camera": "close in from the doorway at chest height, candid documentary distance, nobody in frame",
     "light": "the closet's bare overhead bulb plus green and amber switch LEDs glowing in the shadows",
     "scale_anchor": "a coil of spare cable and a screwdriver on the rack shelf make the panel scale obvious.",
     "lens": "35mm f/2.8 prime, 1/30s"},
    # ---------- NO. 88 (Oct 13, 2026) ----------'''

OLD = "IMAGES = [\n    # ---------- NO. 88 (Oct 13, 2026) ----------"
assert s.count(OLD) == 1, "anchor not unique: %d" % s.count(OLD)
s = s.replace(OLD, NEW)
P.write_text(s, encoding="utf-8")
print("manifest entries added OK")
