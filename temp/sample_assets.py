from PIL import Image
import glob, os
for f in sorted(glob.glob("assets/images/paper-sheet*.png")+glob.glob("assets/images/torn-*.png")+glob.glob("assets/images/composure-hero.jpg")):
    im=Image.open(f).convert("RGB")
    im2=im.resize((40,40))
    px=list(im2.getdata())
    # average of pixels that are not fully transparent-ish (they're png w/ alpha maybe)
    imA=Image.open(f).convert("RGBA").resize((40,40))
    op=[p for p in imA.getdata() if p[3]>200]
    if not op: op=px
    n=len(op)
    r=sum(p[0] for p in op)//n; g=sum(p[1] for p in op)//n; b=sum(p[2] for p in op)//n
    print(f"{os.path.basename(f):45s} {im.size} avg rgb({r},{g},{b}) #{r:02x}{g:02x}{b:02x} opaque%={100*len(op)//1600}")
