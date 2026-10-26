from PIL import Image
import numpy as np
im=Image.open("composure-hero.jpg").convert("RGB")
a=np.asarray(im).astype(float)
print("hero", im.size)
# histogram of hue-ish: find the brightest cluster and mid cluster
lum=(0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2])
flat=a.reshape(-1,3); lf=lum.reshape(-1)
for lo,hi,name in [(0,40,"dark"),(40,90,"mid"),(90,160,"light"),(160,256,"bright")]:
    m=(lf>=lo)&(lf<hi)
    if m.sum(): print(name, round(m.mean(),3), flat[m].mean(axis=0).round(0))
