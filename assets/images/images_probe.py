from PIL import Image
import glob, os
for f in sorted(glob.glob('paper-sheet-semi-rough-*.png'))+sorted(glob.glob('torn-*-strip-*.png')):
    im=Image.open(f).convert('RGBA')
    w,h=im.size
    # sample center and a few points
    px=im.load()
    pts=[(w//2,h//2),(w//4,h//2),(3*w//4,h//2),(w//2,h//4),(w//2,3*h//4)]
    s=[]
    for x,y in pts:
        r,g,b,a=px[x,y]
        s.append('%d,%d,%d a=%d'%(r,g,b,a))
    print(f, im.size, '|', ' | '.join(s))
