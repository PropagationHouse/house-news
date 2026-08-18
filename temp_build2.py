from PIL import Image
import numpy as np

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size

# Crop the paper band: torn top 382 -> clean bottom 681 (299px tall)
band = im.crop((0, 382, w, 681))
arr = np.array(band)
alpha = arr[:,:,3]
bh, bw = alpha.shape  # bh=299 rows, bw=1920 cols

# Fill feather edges horizontally to make full-bleed
for y in range(bh):
    row = alpha[y]
    opaque = np.where(row>128)[0]
    if len(opaque)==0:
        continue
    lo, hi = opaque[0], opaque[-1]
    if lo > 0:
        arr[y, :lo, :3] = arr[y, lo, :3]
        arr[y, :lo, 3] = 255
    if hi < bw-1:
        arr[y, hi+1:, :3] = arr[y, hi, :3]
        arr[y, hi+1:, 3] = 255

band = Image.fromarray(arr)
print('band size:', band.size)  # should be (1920, 299)

# Flip vertically: clean flat bottom -> top (touches hero), torn top -> bottom (hangs into section 01)
band_flip = band.transpose(Image.FLIP_TOP_BOTTOM)
print('flip size:', band_flip.size)

# Trim to 275px tall, centered
w2, h2 = band_flip.size
target_h = 275
top = (h2 - target_h)//2
band_final = band_flip.crop((0, top, w2, top+target_h))
print('final size:', band_final.size)
band_final.save('assets/images/torn-drop-strip.png')

# Verify
a = band_final.split()[3]
fw, fh = band_final.size
print('top rows density (0-5):')
for y in range(6):
    n = sum(1 for x in range(0,fw,8) if a.getpixel((x,y))>128)
    print(f'  y={y}: {n}/{fw//8}')
print('bottom rows density:')
for y in range(fh-6,fh):
    n = sum(1 for x in range(0,fw,8) if a.getpixel((x,y))>128)
    print(f'  y={y}: {n}/{fw//8}')
