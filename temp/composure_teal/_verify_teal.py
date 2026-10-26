import os, json
from playwright.sync_api import sync_playwright

URL = "http://localhost:8099/composure/"
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    fails = []
    pg.on("requestfailed", lambda r: fails.append(r.url))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1200)

    data = pg.evaluate("""() => {
        const g = (sel, prop) => { const e = document.querySelector(sel); return e ? getComputedStyle(e)[prop] : 'MISSING'; };
        const tear = document.querySelector('.paper-tear img');
        const hero = document.querySelector('.hero-paper-img-wrap img');
        return {
            bodyBg: getComputedStyle(document.body).backgroundColor,
            directions: getComputedStyle(document.body).color,
            h1: g('h1','color'),
            kicker: g('p.text-brand-600','color'),
            roomCard: g('.room-card','backgroundColor'),
            plate: g('.plate','backgroundColor'),
            tearSrc: tear ? tear.getAttribute('src') : 'none',
            tearNatural: tear ? tear.naturalWidth + 'x' + tear.naturalHeight : null,
            heroSrc: hero ? hero.getAttribute('src') : 'none',
            heroNatural: hero ? hero.naturalWidth + 'x' + hero.naturalHeight : null,
            roomRows: document.querySelectorAll('.room-row').length,
            shown: document.querySelectorAll('.room-row.is-shown').length,
            hasArchive: !!document.getElementById('archive'),
            hasRooms: !!document.getElementById('rooms'),
            imgCount: document.querySelectorAll('img').length,
            broken: [...document.querySelectorAll('img')].filter(i => !i.complete || i.naturalWidth === 0).map(i => i.getAttribute('src')),
            navArchiveLink: !!document.querySelector('a[href="#archive"]')
        };
    }""")
    print(json.dumps(data, indent=2))
    print("failed requests:", fails if fails else "none")

    # warm-pixel audit: is anything sage/cream still rendering?
    warm = pg.evaluate("""() => {
        const out = [];
        document.querySelectorAll('*').forEach(el => {
            const s = getComputedStyle(el);
            [['color',s.color],['background-color',s.backgroundColor],['border-top-color',s.borderTopColor]].forEach(([k,v])=>{
                const m = v.match(/rgba?\\((\\d+), (\\d+), (\\d+)/);
                if(!m) return;
                const [_,r,g,bb] = m.map(Number);
                if (r > g && r > bb && r - bb > 20) out.push(el.tagName+'.'+(el.className||'').toString().slice(0,40)+' '+k+'='+v);
            });
        });
        return out.slice(0,15);
    }""")
    print("\nwarm/reddish computed colours on page:", warm if warm else "NONE")
    b.close()
