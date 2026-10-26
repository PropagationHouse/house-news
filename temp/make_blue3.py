"""Blue paper: the sheet should read as BLUE paper, not white.
Map paper luminance onto a blue ramp whose brightest stop is a clear light blue."""
from PIL import Image
import numpy as np, os

IMG = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\assets\images"

# brightest stop is a real light blue (#b9d9e7-ish), not white
STOPS = [
    (0.00, (30, 92, 118)),
    (0.40, (108, 170, 196)),
    (0.75, (150, 200, 220)),
    (1.00, (185, 217, 231)),   # light blue paper
]
def ramp(lum):
    lum=np.clip(lum,0,1); out=np.zeros(lum.shape+(3,),float)
    for i in range(len(STOPS)-1):
        p0,c0=STOPS[i]; p1,c1=STOPS[i+1]
        m=(lum>=p0)&(lum<=p1); t=(lum[m]-p0)/(p1-p0)
        for ch in range(3): out[m,ch]=c0[ch]+t*(c1[ch]-c0[ch])
    return out

for src,dst in [("paper-sheet-semi-rough.png","paper-sheet-semi-rough-blue.png"),
                ("torn-up-strip.png","torn-up-strip-blue.png"),
                ("torn-down-strip.png","torn-down-strip-blue.png")]:
    im=Image.open(os.path.join(IMG,src)).convert("RGBA")
    a=np.asarray(im).astype(float); rgb=a[:,:,:3]; al=a[:,:,3]
    lum=(0.299*rgb[:,:,0]+0.587*rgb[:,:,1]+0.114*rgb[:,:,2])/255.0
    out=np.dstack([ramp(lum),al]).astype(np.uint8)
    Image.fromarray(out,"RGBA").save(os.path.join(IMG,dst))
    vis=ramp(lum)[al>10]
    print(dst,"mean",vis.mean(axis=0).round(0))
