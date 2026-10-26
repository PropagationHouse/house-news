from PIL import Image
import numpy as np
im = np.asarray(Image.open("temp/full_after.png").convert("RGB")).astype(float)
prof = im.mean(axis=(1,2))
up_top, up_h = 3053, 206
dn_top, dn_h = 5296, 206
def dump(label, t, h):
    print("==",label)
    for off in range(-30, h+31, 10):
        y = t+off
        if 0<=y<len(prof):
            print("   off %+4d  y=%5d  %.1f" % (off, y, prof[y]))
dump("UP-TEAR (above Products head)", up_top, up_h)
dump("DOWN-TEAR (below composure)", dn_top, dn_h)
