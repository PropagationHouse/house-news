from PIL import Image
im=Image.open('composure-hero.jpg').convert('RGB')
w,h=im.size
print('hero',im.size)
px=im.load()
import collections
c=collections.Counter()
for y in range(0,h,7):
    for x in range(0,w,7):
        r,g,b=px[x,y]
        c[(r//16*16,g//16*16,b//16*16)]+=1
for col,n in c.most_common(8):
    print(col,n)
