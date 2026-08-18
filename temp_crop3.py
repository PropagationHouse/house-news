from PIL import Image

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size
a = im.split()[3]

# Find where bottom becomes flat: scan from last_opaque upward, count when density hits max for 10 consecutive rows
print('rows 665-690 alpha density:')
for y in range(665,691):
    n = sum(1 for x in range(0,w,6) if a.getpixel((x,y))>128)
    bar = '#' * (n*64//(w//6))
    print(f'{y:3d} {bar} {n}')

# Exact transition: find bottom-most fully opaque row
full_rows = [y for y in range(h) if all(a.getpixel((x,y))>128 for x in range(0,w,4))]
print('lowest fully-opaque row:', full_rows[-1] if full_rows else None)
