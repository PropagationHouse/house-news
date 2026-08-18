from PIL import Image
import io, urllib.request

# Check the drop strip's left/right edge opacity at multiple rows to ensure the full-bleed fill worked
r = urllib.request.urlopen('http://localhost:8777/assets/images/torn-drop-strip.png')
im = Image.open(io.BytesIO(r.read())).convert('RGBA')
a = im.split()[3]
w,h = im.size
print('Checking edge opacity for full-bleed fill:')
for y in [20, 80, 140, 200, 240, 260]:
    print(f'  y={y}: left(0)={a.getpixel((0,y))}, x=5={a.getpixel((5,y))}, x=1914={a.getpixel((1914,y))}, right(1919)={a.getpixel((1919,y))}')
