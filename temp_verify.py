from PIL import Image

im = Image.open('assets/images/torn-drop-strip.png').convert('RGBA')
a = im.split()[3]
w,h = im.size

# Print the full alpha ascii for visual verification of the drop shape
rows = 34
cols = 72
for y in range(0,h,max(1,h//rows)):
    row = ''
    for x in range(0,w,max(1,w//cols)):
        p = a.getpixel((x,y))
        ch = '#' if p>200 else ('+' if p>120 else ('.' if p>40 else ' '))
        row += ch
    print(row)
