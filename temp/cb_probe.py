from playwright.sync_api import sync_playwright
import pathlib, json
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(2000)
    el = pg.query_selector(".composure-band")
    el.scroll_into_view_if_needed(); pg.wait_for_timeout(600)
    el.screenshot(path="temp/cb_band.png")
    # zoom the left edge of the cb-visual
    box = pg.eval_on_selector(".composure-band .cb-visual", "e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}}")
    print("cb-visual box", box)
    pg.screenshot(path="temp/cb_left.png", clip={"x":box["x"]-30,"y":box["y"]-10,"width":90,"height":box["h"]+20})
    info = pg.evaluate("""()=>{
      const v=document.querySelector('.composure-band .cb-visual');
      const cs=getComputedStyle(v);
      const img=v.querySelector('img');
      const ics=getComputedStyle(img);
      const before=getComputedStyle(v,'::before');
      return {borderLeft:cs.borderLeft, blw:cs.borderLeftWidth, blc:cs.borderLeftColor, pad:cs.padding,
              imgShadow:ics.boxShadow, beforeBg:before.backgroundImage, beforeShadow:before.boxShadow,
              beforeRect:(()=>{const r=v.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}})(),
              imgRect:(()=>{const r=img.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}})()};
    }""")
    print(json.dumps(info, indent=1))
    b.close()
