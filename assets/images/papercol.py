from PIL import Image
import numpy as np
for f in ["paper-sheet-semi-rough-blue.png","torn-up-strip-blue.png","torn-down-strip-blue.png"]:
    im = Image.open(f).convert("RGBA"); a=np.asarray(im).astype(int)
    alpha=a[...,3]; vis=a[alpha>200][:,:3]
    print(f, im.size, "opaque px", len(vis), "mean RGB", vis.mean(0).round(0) if len(vis) else None, "median", np.median(vis,0) if len(vis) else None)
    # brightest opaque
    lum=vis@np.array([0.2126,0.7152,0.0722])
    print("   lum p5/p50/p95:", np.percentile(lum,[5,50,95]).round(1) if len(vis) else None)
