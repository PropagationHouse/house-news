from PIL import Image

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size
a = im.split()[3]

# For a fully-opaque band row (say y=600), check x extent
row = 600
xs = [x for x in range(w) if a.getpixel((x,row))>128]
print('row 600 opaque x-range:', xs[0], '-', xs[-1], 'count', len(xs), 'of', w)

# Check edges at x=0 and x=1919 for full middle rows
for y in [400,500,600,680]:
    print(f'y={y}: left(0)={a.getpixel((0,y))}, right(1919)={a.getpixel((1919,y))}')

# The existing strips - do they have full 1920 horizontal coverage?
torn_up = Image.open('assets/images/torn-up-strip.png').convert('RGBA')
ta = torn_up.split()[3]
print('torn-up-strip y=100: left', ta.getpixel((0,100)), 'right', ta.getpixel((1919,100)))
torn_down = Image.open('assets/images/torn-down-strip.png').convert('RGBA')
da = torn_down.split()[3]
print('torn-down-strip y=100: left', da.getpixel((0,100)), 'right', da.getpixel((1919,100)))
