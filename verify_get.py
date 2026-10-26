import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width":1280,"height":1000})
        await pg.goto("http://127.0.0.1:8099/composure/index.html", wait_until="networkidle")
        out = await pg.evaluate("""() => {
          const r = [];
          document.querySelectorAll('.buy-card').forEach(c => {
            const cs = getComputedStyle(c);
            const t = c.querySelector('.buy-name'), pr = c.querySelector('.buy-price'), btn = c.querySelector('.buy-btn');
            r.push({name:t.textContent, price:pr.textContent.trim(),
                    bg:cs.backgroundColor, border:cs.borderTopColor, w:Math.round(c.getBoundingClientRect().width),
                    btnBg:getComputedStyle(btn).backgroundColor, btnColor:getComputedStyle(btn).color});
          });
          const sec = document.getElementById('get');
          return {cards:r, secTop:Math.round(sec.getBoundingClientRect().top+scrollY),
                  docW:document.documentElement.scrollWidth, winW:window.innerWidth,
                  h2:document.querySelector('#get h2').textContent.trim(),
                  kicker:document.querySelector('#get .text-brand-600').textContent.trim()};
        }""")
        import json; print(json.dumps(out, indent=1))
        await b.close()
asyncio.run(main())
