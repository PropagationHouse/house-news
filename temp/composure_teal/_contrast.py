from PIL import Image
import os
IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "assets", "images")

def lum(c): return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]

def profile(path, label, bg):
    im = Image.open(path).convert("RGBA")
    im.thumbnail((300, 300))
    vals = [lum(p[:3]) for p in im.get_flattened_data() if p[3] > 180]
    vals.sort()
    lo, mid, hi = vals[int(len(vals)*.05)], vals[len(vals)//2], vals[int(len(vals)*.95)]
    bgl = lum(bg)
    print("%-24s lum  %5.0f / %5.0f / %5.0f   page bg %5.0f   contrast -%.0f / +%.0f"
          % (label, lo, mid, hi, bgl, bgl-lo, hi-bgl))

profile(os.path.join(IMG,"paper-sheet-semi-rough.png"), "sheet (house warm)", (246,241,226))
profile(os.path.join(IMG,"paper-sheet-semi-rough-teal.png"), "sheet (teal)", (231,240,243))
profile(os.path.join(IMG,"torn-up-strip.png"), "tear (house warm)", (246,241,226))
profile(os.path.join(IMG,"torn-up-strip-teal.png"), "tear (teal)", (231,240,243))
