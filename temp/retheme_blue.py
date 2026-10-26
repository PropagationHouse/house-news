"""BLUE pass: make the page + paper genuinely BLUE (not frosted white).
Hue anchored ~200 (app UI family). Raises saturation across the whole light ramp."""
import re, os, shutil

HERE = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news"
SRC = os.path.join(HERE, "composure", "index.html")
BAK = os.path.join(HERE, "temp", "composure_index_pre_blue.html")

# old teal -> new blue
HEX = {
    # brand ramp
    "#eef7f9": "#e4f2f9",
    "#dcecf0": "#c6e3f0",
    "#c6dfe5": "#a4d1e5",
    "#9dcad3": "#72b6d3",
    "#3d8a99": "#3d94bb",
    "#1f6b7a": "#1f7599",
    "#06404c": "#0a5a7d",
    "#05333d": "#084a68",
    "#04282f": "#063a53",
    "#06242c": "#042c40",
    "#041b20": "#021e2c",
    # paper ramp -> genuinely blue
    "#f7fbfc": "#eaf5fa",
    "#e7f0f3": "#cfe6ef",
    "#d7e5e9": "#b9d9e7",
    "#cadde2": "#9cc7da",
    "#bdd2d8": "#7fb4cb",
    "#b2c9cf": "#63a1bc",
    # ink ramp -> blue-black
    "#2a3d44": "#26414d",
    "#20343a": "#1c3540",
    "#162a30": "#142a34",
    "#091d23": "#081d26",
    "#05161b": "#04141b",
    # accent
    "#0e7488": "#0c86a8",
    # caption grey
    "#54707b": "#4d7285",
}
RGBA = {
    "6,64,76": "10,90,125",
    "9,29,35": "8,29,38",
    "42,61,68": "38,65,77",
}

with open(SRC, encoding="utf-8") as f:
    html = f.read()
shutil.copyfile(SRC, BAK)

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
        print("  rgba(%s)->rgba(%s) x%d" % (old, new, n))

# paper assets -> blue variants
html = html.replace("paper-sheet-semi-rough-teal.png", "paper-sheet-semi-rough-blue.png")
html = html.replace("torn-up-strip-teal.png", "torn-up-strip-blue.png")
html = html.replace("torn-down-strip-teal.png", "torn-down-strip-blue.png")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(html)
print("hex rewritten: %d  favicon: %d" % (n_hex, n_enc))
