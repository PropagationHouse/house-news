"""Build genuine BLUE paper assets (duotone anchored on the app UI teal family).

Current -teal assets are near-white (rgb ~220,235,239) = "frosted blue-toned white".
Michael wants the paper itself to read BLUE, like the app UI tone.

Approach: luminance -> 3-stop blue gradient. Alpha preserved.
"""
from PIL import Image
import numpy as np
import os

IMG = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\assets\images"

# 3-stop blue ramp in the app's hue family (hue ~193)
STOPS = [
    (0.00, (16, 62, 78)),     # deep blue shadow
    (0.50, (96, 156, 176)),   # clear mid blue
    (1.00, (226, 241, 246)),  # soft blue-white highlight
]

def ramp(lum):
    lum = np.clip(lum, 0, 1)
    out = np.zeros(lum.shape + (3,), dtype=float)
    for i in range(len(STOPS) - 1):
        p0, c0 = STOPS[i]
        p1, c1 = STOPS[i + 1]
        m = (lum >= p0) & (lum <= p1)
        t = (lum[m] - p0) / (p1 - p0)
        for ch in range(3):
            out[m, ch] = c0[ch] + t * (c1[ch] - c0[ch])
    return out

for src, dst in [
    ("paper-sheet-semi-rough.png", "paper-sheet-semi-rough-blue.png"),
    ("torn-up-strip.png", "torn-up-strip-blue.png"),
    ("torn-down-strip.png", "torn-down-strip-blue.png"),
]:
    im = Image.open(os.path.join(IMG, src)).convert("RGBA")
    a = np.asarray(im).astype(float)
    rgb = a[:, :, :3]
    alpha = a[:, :, 3]
    lum = (0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]) / 255.0
    new = ramp(lum)
    out = np.dstack([new, alpha]).astype(np.uint8)
    Image.fromarray(out, "RGBA").save(os.path.join(IMG, dst))
    vis = new[alpha > 10]
    print(dst, "mean visible RGB", vis.mean(axis=0).round(0))
