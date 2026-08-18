from PIL import Image, ImageStat
import os

def stats(f):
    im = Image.open(f).convert('RGBA')
    w,h = im.size
    a = im.split()[3]
    # masked mean color
    rgb = im.convert('RGB')
    px = list(rgb.getdata())
    ap = list(a.getdata())
    blocked = [(r,g,b) for (r,g,b),aa in zip(px,ap) if aa>128]
    n = len(blocked)
    r = sum(p[0] for p in blocked)/n
    g = sum(p[1] for p in blocked)/n
    b = sum(p[2] for p in blocked)/n
    # sample some row luminance profile
    gray = rgb.convert('L')
    print(f'{os.path.basename(f)[:50]:52s} {w}x{h}  meanRGB=({r:.0f},{g:.0f},{b:.0f})')

for f in ['assets/images/torn-up-strip.png','assets/images/torn-down-strip.png']:
    stats(f)
for f in sorted(os.listdir('assets/paper')):
    stats(os.path.join('assets/paper',f))
