import os, json
from playwright.sync_api import sync_playwright

URL = "http://localhost:8099/composure/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

with sync_playwright() as p:
    b = p.chromium.launch()

    # --- narrow viewport: overflow + anchors ---
    pg = b.new_page(viewport={"width": 390, "height": 844})
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(800)
    over = pg.evaluate("""() => {
        const docW = document.documentElement.clientWidth;
        const bad = [];
        document.querySelectorAll('body *').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > 0 && (r.right > docW + 1 || r.left < -1)) {
                const s = getComputedStyle(el);
                if (s.position === 'fixed') return;
                bad.push({ tag: el.tagName, cls: (el.className||'').toString().slice(0,50),
                           left: Math.round(r.left), right: Math.round(r.right) });
            }
        });
        return { docW, scrollW: document.documentElement.scrollWidth,
                 bodyScrollW: document.body.scrollWidth, offenders: bad.slice(0,10) };
    }""")
    print("MOBILE 390w:", json.dumps(over, indent=2))
    pg.screenshot(path=os.path.join(OUT, "temp", "teal_mobile390.png"), full_page=False)
    pg.close()

    # --- anchors all resolve ---
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto(URL, wait_until="networkidle")
    anchors = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll('a[href^="#"]').forEach(a => {
            const id = a.getAttribute('href').slice(1);
            out.push({ href: '#'+id, exists: !!document.getElementById(id) });
        });
        return out;
    }""")
    print("\nANCHORS:", json.dumps(anchors, indent=2))

    # --- hue comparison: page surface vs app UI bg ---
    hue = pg.evaluate("""() => {
        const toHue = (r,g,b) => {
            r/=255; g/=255; b/=255;
            const mx=Math.max(r,g,b), mn=Math.min(r,g,b), d=mx-mn;
            if(d===0) return 0;
            let h;
            if(mx===r) h=((g-b)/d)%6; else if(mx===g) h=(b-r)/d+2; else h=(r-g)/d+4;
            return Math.round(h*60+360)%360;
        };
        const parse = v => v.match(/\\d+/g).slice(0,3).map(Number);
        const body = parse(getComputedStyle(document.body).backgroundColor);
        const plate = parse(getComputedStyle(document.querySelector('.plate')).backgroundColor);
        return { pageBody: body, pageBodyHue: toHue(...body),
                 pagePlate: plate, pagePlateHue: toHue(...plate),
                 appBg: [6,36,44], appBgHue: toHue(6,36,44),
                 appPanel: [6,64,76], appPanelHue: toHue(6,64,76) };
    }""")
    print("\nHUE MATCH:", json.dumps(hue, indent=2))
    b.close()
