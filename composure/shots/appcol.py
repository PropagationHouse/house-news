from PIL import Image
import numpy as np
im = Image.open("01-timeline.png").convert("RGB")
a = np.asarray(im).astype(int)
print("size", im.size)
h,w,_=a.shape
# top bar strip
bar = a[0:int(h*0.08)].reshape(-1,3)
print("top bar mean", bar.mean(0).round(0))
# body field (avoid panels) - sample right third
body = a[int(h*0.3):int(h*0.9), int(w*0.62):].reshape(-1,3)
print("body mean", body.mean(0).round(0))
# find top colors
flat=a.reshape(-1,3); q=(flat//12*12)
u,c=np.unique(q,axis=0,return_counts=True); idx=np.argsort(-c)[:8]
for i in idx: print("  ", u[i], c[i])
