from PIL import Image
import numpy as np

im = np.array(Image.open('temp/verify_full.png').convert('RGB')).astype(float)
lum = 0.299*im[:,:,0] + 0.587*im[:,:,1] + 0.114*im[:,:,2]
h, w = lum.shape
print('page %dx%d' % (w, h))

FIELD = 42.1

bands = [1691, 3514, 5662, 6767, 8521, 11673, 12696, 13992]
for i, y0 in enumerate(bands):
    a, b = max(0, y0 - 30), min(h, y0 + 200)
    sub = lum[a:b]
    # per-column: first y where lum rises >7 above field (tear edge crossing)
    edges = []
    for x in range(10, w - 10, 8):
        col = sub[:, x]
        idx = np.where(col > FIELD + 7)[0]
        if len(idx):
            edges.append(a + idx[0])
    if not edges:
        print('tear%d  NO EDGE DETECTED' % i); continue
    e = np.array(edges)
    print('tear%-2d edge y  min %5d  max %5d  spread %4d px   n=%d  (of %d cols)' %
          (i, e.min(), e.max(), e.max() - e.min(), len(e), (w - 20)//8))

print()
print('--- tone ladder (median across width) ---')
for label, y in [('field (between bands)', 3200), ('strip solid (tear0)', 1800),
                 ('sheet (hero)', 300), ('below tear0', 1980)]:
    px = tuple(np.median(im[y], axis=0).astype(int))
    print('%-22s y=%5d  rgb%-16s lum %.1f' % (label, y, str(px), np.median(lum[y])))
