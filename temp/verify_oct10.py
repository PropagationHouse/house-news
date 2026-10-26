from playwright.sync_api import sync_playwright
import pathlib
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load")
    pg.wait_for_timeout(1200)
    # substrate visual
    el = pg.query_selector(".feature.substrate .feature-visual")
    if el:
        box = el.bounding_box(); print("substrate box", box)
        st = pg.evaluate("""()=>{const e=document.querySelector('.feature.substrate .feature-visual');const cs=getComputedStyle(e);const be=getComputedStyle(e,'::before');return {bg:cs.backgroundColor,of:cs.overflow,pos:cs.position,tf:be.transform,bbg:be.backgroundImage};}""")
        print("substrate", st)
    # composure band
    cb = pg.query_selector(".composure-band .cb-visual")
    if cb:
        st2 = pg.evaluate("""()=>{const e=document.querySelector('.composure-band .cb-visual');const cs=getComputedStyle(e);const be=getComputedStyle(e,'::before');return {bg:cs.backgroundColor,tf:be.transform,bbg:be.backgroundImage};}""")
        print("composure", st2)
    # torn down
    td = pg.evaluate("""()=>{const e=document.querySelector('.paper-tear:not(.paper-tear-up) img');if(!e)return null;const cs=getComputedStyle(e);return {mask:cs.maskImage||cs.webkitMaskImage};}""")
    print("down-tear", td)
    tu = pg.evaluate("""()=>{const e=document.querySelector('.paper-tear-up img');if(!e)return null;const cs=getComputedStyle(e);return {mask:cs.maskImage||cs.webkitMaskImage};}""")
    print("up-tear", tu)
    b.close()
