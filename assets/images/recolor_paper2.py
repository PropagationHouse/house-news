from PIL import Image, ImageOps
SHEET=(20,66,86)
def colorize(src,dst,target):
    im=Image.open(src).convert('RGB')
    g=ImageOps.autocontrast(ImageOps.grayscale(im),cutoff=1)
    tr,tg,tb=target
    out=Image.merge('RGB',tuple(g.point(lambda v,k=k:int(k*(0.40+0.60*(v/255)))) for k in target))
    a=Image.open(src).convert('RGBA').getchannel('A')
    out=out.convert('RGBA'); out.putalpha(a); out.save(dst)
    print('->',dst,out.size,out.convert('RGB').getpixel((out.size[0]//2,out.size[1]//2)))
colorize('torn-up-strip-blue.png','torn-up-strip-deep.png',SHEET)
colorize('torn-down-strip-blue.png','torn-down-strip-deep.png',SHEET)
