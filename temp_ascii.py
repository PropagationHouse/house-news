from PIL import Image
import os

def ascii_alpha(f, cols=72):
    im = Image.open(f).convert('RGBA')
    w,h = im.size
    a = im.split()[3]
    rows = max(1, cols * h // w // 2)
    print(f'=== {os.path.basename(f)} {w}x{h} ===')
    for y in range(0,h,max(1,h//rows)):
        row = ''
        for x in range(0,w,max(1,w//cols)):
            p = a.getpixel((x,y))
            ch = '#' if p>200 else ('+' if p>120 else ('.' if p>40 else ' '))
            row += ch
        print(row)

for f in ['assets/images/torn-up-strip.png','assets/images/torn-down-strip.png','assets/paper/torn paper facing down.png','assets/paper/torn paper facing up.png']:
    ascii_alpha(f, 72)
