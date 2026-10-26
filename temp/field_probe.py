import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1280, 'height': 900})
        await pg.goto('http://localhost:8099/composure/', wait_until='load')
        await pg.wait_for_timeout(1500)
        info = await pg.evaluate("""()=>{
          const t=[...document.querySelectorAll('.paper-tear')].map(e=>{const r=e.getBoundingClientRect();return {y:r.y+window.scrollY,h:r.height,w:r.width};});
          const h=document.querySelector('.hero-paper-img-wrap');
          const s=document.querySelector('.paper-sheet-deep-navy, .paper-sheet');
          return {tears:t, hero:h?h.getBoundingClientRect().height:null,
                  body:getComputedStyle(document.body).backgroundColor,
                  scene:getComputedStyle(document.body).getPropertyValue('--ui-bg')};
        }""")
        print("INFO", info)
        # sample real pixels down a column through the first tear if present
        if info['tears']:
            y0 = int(info['tears'][0]['y'])
            await pg.evaluate("window.scrollTo(0,%d)" % max(0, y0 - 200))
            await pg.wait_for_timeout(500)
            await pg.screenshot(path='temp/band_now.png')
            for i, t in enumerate(info['tears']):
                print("tear%d y=%d h=%d" % (i, t['y'], t['h']))
            print("tear y-offsets between pairs:", [info['tears'][i+1]['y'] - info['tears'][i]['y'] for i in range(len(info['tears'])-1)])
        await b.close()

asyncio.run(main())
