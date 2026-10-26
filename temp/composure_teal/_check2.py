import os, json
from PIL import Image
from playwright.sync_api import sync_playwright

URL = "http://localhost:8099/composure/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(URL, wait_until="networkidle")
    n = pg.evaluate("""() => {
        const docW = document.documentElement.clientWidth;
        let count = 0, worst = null, worstOver = 0;
        document.querySelectorAll('body *').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > 0 && r.right > docW + 1) {
                if (getComputedStyle(el).position === 'fixed') return;
                count++;
                const over = Math.round(r.right - docW);
                if (over > worstOver) { worstOver = over; worst = (el.className||el.tagName).toString().slice(0,50); }
            }
        });
        return { count, worstOver, worst, scrollW: document.documentElement.scrollWidth };
    }""")
    print("mobile 390 overflow:", json.dumps(n))
    b.close()

# hero sheet vs page bg contrast, sampled from the render
im = Image.open(os.path.join(OUT, "temp", "teal_hero.png")).convert("RGB")
w, h = im.size
def avg(box):
    c = im.crop(box); px = list(c.get_flattened_data())
    n = len(px)
    return tuple(round(sum(p[i] for p in px)/n) for i in range(3))
print("\nhero render 1440x900")
print("  top-left corner (page bg) :", avg((0, 0, 200, 120)))
print("  centre band (paper sheet) :", avg((560, 120, 880, 240)))
print("  bottom edge (page bg)     :", avg((0, 820, 300, 899)))
