import asyncio, json
from playwright.async_api import async_playwright
URL="http://localhost:8099/composure/"
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch()
        pg=await b.new_page(viewport={"width":1440,"height":1000})
        await pg.goto(URL, wait_until="networkidle", timeout=60000)
        await pg.wait_for_timeout(1200)
        r=await pg.evaluate("""() => {
          const out={};
          out.bodyBg=getComputedStyle(document.body).backgroundColor;
          out.bodyColor=getComputedStyle(document.body).color;
          out.h2s=Array.from(document.querySelectorAll('h2')).map(h=>h.innerText.replace(/\\n/g,' '));
          out.roomCount=document.querySelectorAll('.room-row').length;
          out.shownCount=document.querySelectorAll('.room-row.is-shown').length;
          out.imgCount=document.images.length;
          out.broken=Array.from(document.images).filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src'));
          const warm=[];
          document.querySelectorAll('*').forEach(el=>{const c=getComputedStyle(el);
            [c.color,c.backgroundColor,c.borderTopColor].forEach(v=>{const m=v&&v.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
              if(m){const r=+m[1],g=+m[2],bl=+m[3]; if(r>g&&r>bl&&r>90&&(r-Math.max(g,bl))>25) warm.push(el.tagName+' '+v);}});});
          out.warmCount=warm.length; out.warmSample=warm.slice(0,6);
          out.scrollH=document.body.scrollHeight;
          return out;
        }""")
        print(json.dumps(r, indent=1))
        await b.close()
asyncio.run(main())
