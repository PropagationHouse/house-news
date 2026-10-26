from PIL import Image
import numpy as np, os
IMG=r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\assets\images"
# Deeper, genuinely BLUE paper stock - not blue-toned white.
STOPS=[(0.00,(6,38,62)),(0.40,(32,92,134)),(0.75,(60,125,172)),(1.00,(95,160,200))]
def ramp(l):
    l=np.clip(l,0,1);o=np.zeros(l.shape+(3,),float)
    for i in range(len(STOPS)-1):
        p0,c0=STOPS[i];p1,c1=STOPS[i+1];m=(l>=p0)&(l<=p1);t=(l[m]-p0)/(p1-p0)
        for ch in range(3):o[m,ch]=c0[ch]+t*(c1[ch]-c0[ch])
    return o
for src,dst in [("paper-sheet-semi-rough.png","paper-sheet-semi-rough-blue.png"),
                ("torn-up-strip.png","torn-up-strip-blue.png"),
                ("torn-down-strip.png","torn-down-strip-blue.png")]:
    im=Image.open(os.path.join(IMG,src)).convert("RGBA")
    a=np.asarray(im).astype(float);rgb=a[:,:,:3];al=a[:,:,3]
    lum=(0.299*rgb[:,:,0]+0.587*rgb[:,:,1]+0.114*rgb[:,:,2])/255.0
    out=ramp(lum)
    Image.fromarray(np.dstack([out,al]).astype(np.uint8),"RGBA").save(os.path.join(IMG,dst))
    vis=out[al>128]
    print(dst, vis.mean(axis=0).round(0), "sat", round((vis.max(1)-vis.min(1)).mean()/vis.max(),2))
