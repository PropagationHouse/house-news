import asyncio, os
from playwright.async_api import async_playwright

OUT = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp"
URL = "http://localhost:8099/composure/"

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1440,"height":1000}, device_scale_factor=1)
        errs=[]
        pg.on("console", lambda m: errs.append(m.text) if m.type=="error" else None)
        pg.on("requestfailed", lambda r: errs.append("REQFAIL "+r.url))
        await pg.goto(URL, wait_until="networkidle", timeout=60000)
        await pg.wait_for_timeout(1500)
        # full page
        await pg.screenshot(path=os.path.join(OUT,"cur_full.png"), full_page=True)
        # rooms section
        el = await pg.query_selector("#rooms")
        if el: await el.screenshot(path=os.path.join(OUT,"cur_rooms.png"))
        # hero
        await pg.screenshot(path=os.path.join(OUT,"cur_hero.png"))
        # metrics
        h = await pg.evaluate("document.body.scrollHeight")
        imgs = await pg.evaluate("Array.from(document.images).filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
        print("scrollHeight", h)
        print("broken imgs", imgs)
        print("console errors", errs[:10])
        await b.close()

asyncio.run(main())
