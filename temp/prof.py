from PIL import Image
import numpy as np
for name,label in [("temp/tear_up_after.png","UP"),("temp/tear_down_after.png","DOWN")]:
    im = np.asarray(Image.open(name).convert("RGB")).astype(float)
    # column mean brightness per row
    prof = im.mean(axis=(1,2))
    # find the tear band: rows where variance across x is high (the ragged paper)
    var = im.std(axis=(1,2))
    print("==",label, im.shape)
    # print brightness profile around the tear
    print("brightness min/max:", round(prof.min(),1), round(prof.max(),1))
    # sharpest single-row jump
    d = np.abs(np.diff(prof))
    print("max row-to-row jump:", round(d.max(),2), "at row", int(d.argmax()))
    print("mean jump:", round(d.mean(),3))
