"""Stronger BLUE pass: raise saturation on the light ramp so surfaces read blue, not white.
Hue anchored at 194 (app UI). Keeps the dark brand ramp (that already matches the UI)."""
from PIL import Image
import numpy as np, os

IMG = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\assets\images"

# blue paper ramp, hue 194, genuinely saturated
STOPS = [
    (0.00, (24, 78, 96)),     # deep blue shadow
    (0.35, (86, 150, 172)),   # mid blue
    (0.70, (150, 198, 214)),  # light blue
    (1.00, (222, 240, 246)),  # blue-white highlight
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
    print(dst,"mean",vis.mean(axis=0).round(0),"p10",np.percentile(vis,10,axis=0).round(0),"p90",np.percentile(vis,90,axis=0).round(0))
