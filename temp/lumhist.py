from PIL import Image
import numpy as np
im=Image.open("paper-sheet-semi-rough.png").convert("RGBA")
a=np.asarray(im).astype(float); rgb=a[:,:,:3]; al=a[:,:,3]
lum=(0.299*rgb[:,:,0]+0.587*rgb[:,:,1]+0.114*rgb[:,:,2])/255.0
v=lum[al>10]
print("lum p5/p25/p50/p75/p95", [round(np.percentile(v,p),2) for p in (5,25,50,75,95)])
