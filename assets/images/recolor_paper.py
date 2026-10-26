from PIL import Image, ImageOps
import os

def colorize(src, dst, target, keep_alpha=True):
    im = Image.open(src).convert('RGB')
    g = ImageOps.grayscale(im)                      # keep fiber texture + shading
    # normalize the grey range so texture survives
    g = ImageOps.autocontrast(g, cutoff=1)
    tr,tg,tb = target
    out = Image.merge('RGB', (
        g.point(lambda v: int(tr*(0.35+0.65*(v/255)))),
        g.point(lambda v: int(tg*(0.35+0.65*(v/255)))),
        g.point(lambda v: int(tb*(0.35+0.65*(v/255)))),
    ))
    a = Image.open(src).convert('RGBA').getchannel('A')
    out = out.convert('RGBA'); out.putalpha(a)
    out.save(dst)
    print('->', dst, out.size, 'sample', out.convert('RGB').load()[out.size[0]//2,out.size[1]//2])

# sheet tone: same family as field (#06242c), lifted so white type reads clearly
SHEET = (20, 66, 86)
EDGE  = (12, 48, 64)

colorize('paper-sheet-semi-rough-navy.png', 'paper-sheet-deep-navy.png', SHEET)
colorize('torn-up-strip-blue.png',   'torn-up-strip-deep.png',   EDGE)
colorize('torn-down-strip-blue.png', 'torn-down-strip-deep.png', EDGE)
