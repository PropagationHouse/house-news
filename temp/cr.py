from PIL import Image
def lum(rgb):
    def f(c):
        c=c/255
        return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    r,g,b=rgb
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    l1,l2=sorted([lum(a),lum(b)],reverse=True)
    return (l1+0.05)/(l2+0.05)
field=(6,36,44)
bg_white="""white on field"""
# panel over field: 0.055 white over #06242c
def over(fg,a,bg): return tuple(round(fg[i]*a+bg[i]*(1-a)) for i in range(3))
panel=over((255,255,255),0.055,field)
panel_w=over((255,255,255),0.04,field)
sheet=(17,58,76)
print('field',field,'lum',round(lum(field),3))
print('panel',panel,'lum',round(lum(panel),3))
print('sheet',sheet,'lum',round(lum(sheet),3))
print('white/field   %.1f'%cr((255,255,255),field))
print('white/panel   %.1f'%cr((255,255,255),panel))
print('white/roomcard %.1f'%cr((255,255,255),panel_w))
print('soft80/field  %.1f'%cr(over((226,242,250),0.80,field),field))
print('soft80/panel  %.1f'%cr(over((226,242,250),0.80,panel),panel))
print('accent/field  %.1f'%cr((127,212,236),field))
print('accent/panel  %.1f'%cr((127,212,236),panel))
print('white/sheet   %.1f'%cr((255,255,255),sheet))
print('accent/sheet  %.1f'%cr((127,212,236),sheet))
# sheet art background actually rendered
im=Image.open('assets/images/paper-sheet-deep-navy.png').convert('RGB')
print('sheet art sample',im.getpixel((im.size[0]//2,im.size[1]//2)))
