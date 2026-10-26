import asyncio, sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":1000})
        await pg.goto("http://127.0.0.1:8099/composure/index.html", wait_until="networkidle")
        await pg.evaluate("document.getElementById('get').scrollIntoView()")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path=r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp\get_section.png")
        # sanity: count buy cards + buttons
        n = await pg.evaluate("document.querySelectorAll('.buy-card').length")
        btns = await pg.evaluate("Array.from(document.querySelectorAll('.buy-btn')).map(a=>a.textContent.trim()+' | '+a.getAttribute('href'))")
        print("buy cards:", n)
        for x in btns: print("  ", x)
        # check nav + CTA
        print("nav Get It:", await pg.evaluate("!!document.querySelector('nav a[href=\"#get\"]')"))
        print("cta primary:", await pg.evaluate("document.querySelectorAll('section .bg-brand-600')[0].textContent.trim()"))
        await b.close()
asyncio.run(main())
