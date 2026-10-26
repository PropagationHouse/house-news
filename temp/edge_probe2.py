from PIL import Image
import numpy as np
# cb-visual left edge lands at band-screenshot x ~= 634 (page 777.5 - band left 143)
for f in ["temp/cb_band.png","temp/cb_band_after.png"]:
    im = np.asarray(Image.open(f).convert("RGB")).astype(int)
    print(f)
    for x in range(630,642):
        col = im[:,x,:]
        print("   x=%d mean=%s std=%.1f" % (x, np.round(col.mean(axis=0),0).astype(int).tolist(), col.std()))
