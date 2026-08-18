from PIL import Image

im = Image.open('assets/paper/thin wheatpasted torn poster paper divider, torn edge top, clean flat bottom.png').convert('RGBA')
w,h = im.size
a = im.split()[3]

# ragged top zone is 381 - some rows; inspect 375-400
print('rows 375-410, alpha density:')
for y in range(375,411):
    n = sum(1 for x in range(0,w,6) if a.getpixel((x,y))>128)
    bar = '#' * (n*64//(w//6))
    print(f'{y:3d} {bar} {n}')
