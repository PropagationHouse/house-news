import asyncio
from playwright.async_api import async_playwright

def lum(p):
    return 0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1280, 'height': 900})
        errs = []
        pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://localhost:8099/composure/', wait_until='load')
        await pg.wait_for_timeout(1500)

        base = await pg.evaluate("""()=>{
          const rects=[...document.querySelectorAll('.paper-tear')].map(e=>e.getBoundingClientRect().top+window.scrollY);
          return {tears:rects, bg:getComputedStyle(document.body).backgroundColor};
        }""")
        print('body bg   :', base['bg'])
        print('tear count:', len(base['tears']))

        # full page shot
        await pg.screenshot(path='temp/verify_full.png', full_page=True)

        # zoom on first tear band: 250px above to 250px below
        y = int(base['tears'][0])
        await pg.evaluate("window.scrollTo(0,%d)" % max(0, y - 260))
        await pg.wait_for_timeout(400)
        await pg.screenshot(path='temp/verify_band0.png')

        imgs = await pg.evaluate("""()=>{
          const out=[];
          document.querySelectorAll('img').forEach(i=>{ if(!i.complete||i.naturalWidth===0) out.push(i.getAttribute('src')); });
          return {broken:out, total:document.querySelectorAll('img').length};
        }""")
        print('images    :', imgs['total'], 'broken:', imgs['broken'])
        print('console   :', errs if errs else 'clean')
        await b.close()

asyncio.run(main())
