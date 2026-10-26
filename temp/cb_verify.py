from playwright.sync_api import sync_playwright
import pathlib, json
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(2000)
    el = pg.query_selector(".composure-band")
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    el.screenshot(path="temp/cb_band_after.png")
    info = pg.evaluate("""()=>{
      const v=document.querySelector('.composure-band .cb-visual');
      const cs=getComputedStyle(v);
      const before=getComputedStyle(v,'::before');
      const r=v.getBoundingClientRect();
      return {borderLeft:cs.borderLeft, borderTop:cs.borderTop, beforeBg:before.backgroundImage.slice(0,60),
              beforeShadow:before.boxShadow, rect:{x:r.x,y:r.y,w:r.width,h:r.height}};
    }""")
    print(json.dumps(info, indent=1))
    # also confirm the other 4 sheets still clean
    print("rotate hits:", pg.evaluate("()=>document.documentElement.outerHTML.split('rotate(').length-1"))
    b.close()
