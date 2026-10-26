from PIL import Image
import numpy as np
for f in ["paper-sheet-semi-rough-blue.png","paper-sheet-semi-rough-teal.png","torn-up-strip-blue.png","torn-up-strip-teal.png"]:
    im=Image.open("assets/images/"+f).convert("RGBA")
    a=np.asarray(im).astype(int)
    op=a[...,3]>128
    px=a[...,:3][op]
    print(f"{f:36s} size={im.size} opaque%={100*op.mean():.1f} mean={px.mean(0).round(0)} p10={np.percentile(px,10,0).round(0)} p90={np.percentile(px,90,0).round(0)}")
