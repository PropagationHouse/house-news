"""Re-theme composure/index.html from house sage to the app's teal family.

Anchored on real pixel values from the Composure UI captures:
  #06242c  app background          -> brand-900
  #06404c  bright panel            -> brand-600
  #05333d  top bar                 -> brand-700
Light page surfaces are built in the same hue so the whole page reads as the app.
"""
import re
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "index.html")
BAK = os.path.join(HERE, "..", "temp", "composure_index_pre_teal.html")

HEX = {
    # brand ramp (sage -> teal)
    "#faf7f0": "#eef7f9",
    "#f3eeda": "#dcecf0",
    "#e6e0c4": "#c6dfe5",
    "#d4cc9a": "#9dcad3",
    "#8a9a4f": "#3d8a99",
    "#6b7d38": "#1f6b7a",
    "#4b5320": "#06404c",
    "#3a4018": "#05333d",
    "#2c3112": "#04282f",
    "#1f240d": "#06242c",
    "#141806": "#041b20",
    # paper ramp (warm cream -> cool teal paper)
    "#fdfbf4": "#f7fbfc",
    "#f6f1e2": "#e7f0f3",
    "#ece5cf": "#d7e5e9",
    "#e0d8bf": "#cadde2",
    "#d3c9a8": "#bdd2d8",
    "#c8c3ad": "#b2c9cf",
    # ink ramp (olive-black -> blue-black)
    "#3a3d2e": "#2a3d44",
    "#2f3126": "#20343a",
    "#24271c": "#162a30",
    "#1a1d12": "#091d23",
    "#11140c": "#05161b",
    # secondary accent (old gold -> bright cyan-teal)
    "#8a7a2f": "#0e7488",
    # caption grey
    "#6b6e5a": "#54707b",
}

RGBA = {
    "75,83,32": "6,64,76",
    "26,29,18": "9,29,35",
    "58,61,46": "42,61,68",
}

with open(SRC, encoding="utf-8") as f:
    html = f.read()

shutil.copyfile(SRC, BAK)

# hex tokens (case-insensitive) + url-encoded favicon forms
def sub_hex(m):
    tok = "#" + m.group(1).lower()
    return HEX.get(tok, m.group(0))

html, n_hex = re.subn(r"#([0-9a-fA-F]{6})\b", sub_hex, html)

def sub_enc(m):
    tok = "#" + m.group(1).lower()
    rep = HEX.get(tok)
    return "%23" + rep[1:] if rep else m.group(0)

html, n_enc = re.subn(r"%23([0-9a-fA-F]{6})\b", sub_enc, html)

for old, new in RGBA.items():
    n = html.count(old)
    if n:
        html = html.replace(old, new)
        print("  rgba(%s) -> rgba(%s)  x%d" % (old, new, n))

# paper assets -> teal duotone variants
html = html.replace("paper-sheet-semi-rough.png", "paper-sheet-semi-rough-teal.png")
html = html.replace("torn-up-strip.png", "torn-up-strip-teal.png")
html = html.replace("torn-down-strip.png", "torn-down-strip-teal.png")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(html)

print("hex tokens rewritten: %d   favicon-encoded: %d" % (n_hex, n_enc))
print("backup -> %s" % os.path.relpath(BAK, HERE))

# anything warm left?
leftovers = set(re.findall(r"#([0-9a-fA-F]{6})\b", html))
warm = [c for c in leftovers if c.lower() in
        ("4b5320", "f6f1e2", "1a1d12", "8a7a2f", "ece5cf", "8a9a4f", "6b7d38")]
print("warm leftovers:", warm if warm else "none")
