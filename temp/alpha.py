from PIL import Image
import numpy as np
for n in ["paper-sheet-semi-rough.png","torn-up-strip.png","torn-down-strip.png","paper-sheet-semi-rough-teal.png"]:
    im=Image.open(n)
    print(n, im.mode, im.size)
    if im.mode=="RGBA":
        a=np.asarray(im)[:,:,3]
        print("   alpha min/max", a.min(), a.max(), "frac transparent", round((a<10).mean(),3))
