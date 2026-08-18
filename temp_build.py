from PIL import Image

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size
a = im.split()[3]

# Crop the paper band: torn top 382 -> clean bottom 681 (300px tall)
band = im.crop((0, 382, w, 681))
print('crop size:', band.size)

# Check the band edges — left/right are slightly feathered. 
# Extend the edge pixels horizontally to make it full-bleed like the existing strips
# Strategy: for each row, find leftmost/rightmost opaque pixel, and fill outward
import numpy as np
arr = np.array(band)
alpha = arr[:,:,3]
h,w = alpha.shape

# for each row, fill left side from first opaque to x=0 and right side from last opaque to w-1
for y in range(h):
    row = alpha[y]
    opaque = np.where(row>128)[0]
    if len(opaque)==0:
        continue
    lo, hi = opaque[0], opaque[-1]
    # fill from 0..lo and hi..w-1 with the mean color of the row's edge pixels
    if lo > 0:
        arr[y, :lo, :3] = arr[y, lo, :3]
        arr[y, :lo, 3] = 255
    if hi < w-1:
        arr[y, hi+1:, :3] = arr[y, hi, :3]
        arr[y, hi+1:, 3] = 255

band = Image.fromarray(arr)

# Now flip vertically: clean bottom (flat, opaque) becomes TOP (touching hero), torn top becomes BOTTOM (hanging into section 01)
band_flip = band.transpose(Image.FLIP_TOP_BOTTOM)

# Trim to 275px height to match existing strips, centered on the band
target_h = 275
bh, bw = band_flip.size
top = (bh - target_h)//2
band_final = band_flip.crop((0, top, bw, top+target_h))

band_final.save('assets/images/torn-drop-strip.png')
print('saved torn-drop-strip.png', band_final.size)

# Verify alpha profile of final strip (top should be clean/flat, bottom ragged)
a = band_final.split()[3]
print('final top 5 rows density:')
for y in range(5):
    n = sum(1 for x in range(0,bw,8) if a.getpixel((x,y))>128)
    print(f'  y={y}: {n}/{bw//8}')
print('final bottom 5 rows density:')
bh2 = band_final.size[1]
for y in range(bh2-5,bh2):
    n = sum(1 for x in range(0,bw,8) if a.getpixel((x,y))>128)
    print(f'  y={y}: {n}/{bw//8}')
