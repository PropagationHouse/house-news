from PIL import Image
import os
base=r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\assets\images"
for f in ["paper-sheet-semi-rough-teal.png","torn-up-strip-teal.png","torn-down-strip-teal.png","composure-hero.jpg"]:
    p=os.path.join(base,f)
    if not os.path.exists(p): print(f,"MISSING"); continue
    im=Image.open(p).convert("RGB")
    small=im.resize((60,60))
    px=list(small.getdata())
    # average of opaque-ish pixels
    r=sum(p[0] for p in px)//len(px); g=sum(p[1] for p in px)//len(px); b=sum(p[2] for p in px)//len(px)
    import colorsys
    h,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
    print(f"{f:38s} {im.size} avg rgb({r},{g},{b}) hue={h*360:.0f}")
