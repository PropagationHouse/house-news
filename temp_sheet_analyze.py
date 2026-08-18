"""Analyze paper sheet assets: tone, texture variance, edge raggedness (alpha) per side."""
import os
from PIL import Image, ImageStat

FOLDER = r"assets\paper"
OUT = "temp_sheet_report.txt"

def edge_alpha(img, side, inset=4):
    w, h = img.size
    a = []
    if side in ("top", "bottom"):
        y = inset if side == "top" else h - inset - 1
        step = max(1, w // 240)
        a = [img.getpixel((x, y))[3] for x in range(0, w, step)]
    else:
        x = inset if side == "left" else w - inset - 1
        step = max(1, h // 240)
        a = [img.getpixel((x, y))[3] for y in range(0, h, step)]
    opaque = sum(1 for v in a if v > 200)
    semi = sum(1 for v in a if 20 <= v <= 200)
    transparent = sum(1 for v in a if v < 20)
    # raggedness = transitions between opaque/transparent along the edge
    trans = 0
    for i in range(1, len(a)):
        if (a[i] > 200) != (a[i - 1] > 200):
            trans += 1
    return opaque, semi, transparent, trans

def main():
    for f in sorted(os.listdir(FOLDER)):
        if not f.lower().endswith((".png", ".jpg")):
            continue
        p = os.path.join(FOLDER, f)
        img = Image.open(p).convert("RGBA")
        w, h = img.size
        stat = ImageStat.Stat(img.convert("RGB"))
        mean = tuple(round(v, 1) for v in stat.mean)
        std = tuple(round(v, 1) for v in stat.stddev)
        edges = {}
        for side in ("top", "bottom", "left", "right"):
            op, semi, tr, ragg = load_alpha(img, side)
            edges[side] = (op, semi, tr, ragg)
        print(f"{f}")
        print(f"  size={w}x{h} avg_rgb={mean} std={std}")
        for side in ("top", "bottom", "left", "right"):
            op, semi, tr, ragg = edges[side]
            print(f"  {side:6s} opaque={op:3d} semi={semi:3d} clear={tr:3d} ragged={ragg:3d}")

if __name__ == "__main__":
    main()