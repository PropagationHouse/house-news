from PIL import Image
import collections
im=Image.open(r'temp\dark_full.png').convert('RGB'); w,h=im.size
def top(region,n=5):
    c=collections.Counter()
    for y in range(0,region.size[1],3):
        for x in range(0,region.size[0],3):
            c[region.getpixel((x,y))]+=1
    return [(col,round(100*nn/((region.size[0]//3)*(region.size[1]//3)),1)) for col,nn in c.most_common(n)]
bands={'hero':(0,1000),'heronav':(0,120),'img':(1000,1700),'two':(1700,4600),'collab':(4600,7000),
       'daw':(7000,8600),'notation':(8600,10200),'sound':(10200,12600),'pocket':(12600,13600),
       'rooms':(13600,14700),'cta':(14700,15124)}
for k,(a,b) in bands.items():
    print(k, top(im.crop((0,a,w,min(b,h))),4))
