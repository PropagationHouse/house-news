from PIL import Image

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size
a = im.split()[3]

# find first opaque row (torn top edge) and last fully-opaque row
first = None
last = None
for y in range(h):
    row_alpha = 0
    for x in range(0,w,8):
        if a.getpixel((x,y)) > 128:
            row_alpha += 1
    if row_alpha > 0:
        if first is None: first = y
        last = y
print('size', im.size, 'first_opaque', first, 'last_opaque', last)

# Profile the raggedness: for each row count opaque pixels
# Print a downsampled top 50 rows to see the raggedness zone
print('top 40 rows alpha density (0-32):')
for y in range(0,40):
    n = sum(1 for x in range(0,w,6) if a.getpixel((x,y))>128)
    print(f'{y:3d} {"#"* (n*64//(w//6))} {n}')
