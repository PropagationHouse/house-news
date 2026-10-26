from PIL import Image
import numpy as np

BASE = np.array([18,61,80], dtype=float)   # EXACTLY the sheet tone (paper-sheet-deep-navy) - tear is the same stock as the sheet

def retint(src, dst, base):
    im = Image.open(src).convert('RGBA')
    a = np.array(im).astype(float)
    alpha = a[:,:,3]
    lum = a[:,:,:3].mean(axis=2)
    op = alpha > 200
    if op.sum() > 50:
        lo, hi = np.percentile(lum[op], 2), np.percentile(lum[op], 98)
    else:
        lo, hi = lum.min(), lum.max()
    n = np.clip((lum - lo) / max(hi-lo, 1.0), 0, 1)
    f = 0.90 + 0.16 * n                      # subtle fiber texture around base
    out = np.zeros(a.shape, dtype=np.uint8)
    for i in range(3):
        out[:,:,i] = np.clip(base[i] * f, 0, 255).astype(np.uint8)
    out[:,:,3] = alpha.astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(dst)
    o = np.array(Image.open(dst).convert('RGBA'))
    m = o[:,:,3] > 200
    med = np.median(o[:,:,:3][m], axis=0)
    print(f"{dst}: opaque median RGB={med} lum={0.2126*med[0]+0.7152*med[1]+0.0722*med[2]:.1f} opaque_px={m.sum()}")

retint('torn-up-strip-blue.png',   'torn-up-strip-deep.png',   BASE)
retint('torn-down-strip-blue.png', 'torn-down-strip-deep.png', BASE)

# reference: what the sheet actually renders at
s = np.array(Image.open('paper-sheet-deep-navy.png').convert('RGBA'))
sm = s[:,:,3] > 200
smed = np.median(s[:,:,:3][sm], axis=0)
print("SHEET paper-sheet-deep-navy.png opaque median RGB=", smed, "lum=%.1f" % (0.2126*smed[0]+0.7152*smed[1]+0.0722*smed[2]))
