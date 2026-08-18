"""Print alpha profiles for each paper sheet so I can see which has a ragged bottom usable as a barrier."""
import os
from PIL import Image

FOLDER = r"assets\paper"

def row_coverage(a, w, y):
    step = max(1, w // 200)
    tot = op = 0
    for x in range(0, w, step):
        v = a.getpixel((x, y))
        tot += 1
        if v > 200:
            op += 1
    return round(100 * op / tot)

def col_coverage(a, h, x):
    step = max(1, h // 200)
    tot = op = 0
    for y in range(0, h, step):
        v = a.getpixel((x, y))
        tot += 1
        if v > 200:
            op += 1
    return round(100 * op / tot)

def main():
    for f in sorted(os.listdir(FOLDER)):
        if not f.lower().endswith('.png'):
            continue
        img = Image.open(os.path.join(FOLDER, f)).convert('RGBA')
        w, h = img.size
        a = img.getchannel('A')
        bbox = a.getbbox()
        print(f'=== {f}  {w}x{h}  bbox={bbox}')
        tops = [row_coverage(a, w, y) for y in [0, 5, 15, 30, 60, 120, 200]]
        bottoms = [row_coverage(a, w, y) for y in [h-1, h-5, h-15, h-30, h-60, h-120, h-200]]
        lefts = [col_coverage(a, h, x) for x in [0, 5, 15, 30, 60, 120]]
        rights = [col_coverage(a, h, x) for x in [w-1, w-5, w-15, w-30, w-60, w-120]]
        print('  top    coverage%:', tops)
        print('  bottom coverage%:', bottoms)
        print('  left   coverage%:', lefts)
        print('  right  coverage%:', rights)

if __name__ == '__main__':
    main()