from PIL import Image
import numpy as np
for f in ["temp/cb_band.png","temp/cb_band_after.png"]:
    im = np.asarray(Image.open(f).convert("RGB")).astype(int)
    h,w,_ = im.shape
    # cb-visual starts at x=777.5 in page coords; band screenshot starts at band x
    # find the leftmost column that is the sheet (paper ~ (245,242,230)); scan columns
    col_means = im.mean(axis=0)
    # report first 6 columns' mean brightness and the darkest column in first 40
    print(f, "shape", im.shape)
    print("  first 6 col means:", [round(float(col_means[i].mean()),1) for i in range(6)])
    seg = col_means[:40]
    print("  darkest col in first 40:", int(seg.argmin()), round(float(seg.min()),1))
    # vertical-line detector: column whose std across rows is tiny but differs from neighbours
    stds = im.std(axis=0).mean(axis=1)
    print("  min col std first 40:", round(float(stds[:40].min()),1), "at", int(stds[:40].argmin()))
