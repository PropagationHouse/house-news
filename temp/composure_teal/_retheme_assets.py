"""Composure page re-theme: duotone the paper assets into the app's teal family.

Writes NEW files (*-teal.png) so the warm house paper stays intact for other pages.
"""
from PIL import Image
import os

# Anchored on the real app UI: bg #06242c, bright panel #06404c, card #07252f / #0f2c34
SHEET_DARK = (176, 210, 218)   # #c6dfe3  shadowed paper
SHEET_LIGHT = (252, 254, 254)  # #fbfefe  lit paper

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "..", "..", "assets", "images")

TARGETS = [
    "paper-sheet-semi-rough.png",
    "torn-up-strip.png",
    "torn-down-strip.png",
]


def duotone(src, dst):
    im = Image.open(src).convert("RGBA")
    w, h = im.size
    px = list(im.get_flattened_data())

    lums = []
    for r, g, b, a in px:
        if a > 180:
            lums.append(0.299 * r + 0.587 * g + 0.114 * b)
    lums.sort()
    lo = lums[int(len(lums) * 0.03)]
    hi = lums[int(len(lums) * 0.97)]

    out = []
    for r, g, b, a in px:
        if a == 0:
            out.append((0, 0, 0, 0))
            continue
        lum = 0.299 * r + 0.587 * g + 0.114 * b
        t = (lum - lo) / (hi - lo) if hi > lo else 0.5
        t = 0.0 if t < 0 else (1.0 if t > 1 else t)
        nr = round(SHEET_DARK[0] + (SHEET_LIGHT[0] - SHEET_DARK[0]) * t)
        ng = round(SHEET_DARK[1] + (SHEET_LIGHT[1] - SHEET_DARK[1]) * t)
        nb = round(SHEET_DARK[2] + (SHEET_LIGHT[2] - SHEET_DARK[2]) * t)
        out.append((nr, ng, nb, a))

    res = Image.new("RGBA", (w, h))
    res.putdata(out)
    res.save(dst)
    print("  %-34s -> %s  (%dx%d, lum %.0f-%.0f)" % (os.path.basename(src), os.path.basename(dst), w, h, lo, hi))


print("Duotoning paper assets to teal:")
for name in TARGETS:
    src = os.path.join(IMG, name)
    base, ext = os.path.splitext(name)
    dst = os.path.join(IMG, base + "-teal" + ext)
    duotone(src, dst)

# Report the logo mark colour so we know whether it clashes on a cool page
mark = os.path.join(HERE, "..", "substrate-v2", "ph-mark-dark.png")
if os.path.exists(mark):
    im = Image.open(mark).convert("RGBA")
    im.thumbnail((64, 64))
    from collections import Counter
    c = Counter([p[:3] for p in im.get_flattened_data() if p[3] > 150])
    print("\nph-mark-dark.png dominant opaque colours:")
    for col, n in c.most_common(5):
        print("   #%02x%02x%02x  x%d" % (col[0], col[1], col[2], n))
