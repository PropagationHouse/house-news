import sys
from playwright.sync_api import sync_playwright
OUT=sys.argv[1] if len(sys.argv)>1 else "before"
URL="file:///C:/Users/Bl0ck/Desktop/desk/org/Propagation%20House%20Website%20Rebuild/house-news/index.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":1100}, device_scale_factor=1)
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(1800)
    # regions
    def box(sel):
        return pg.evaluate("""(s)=>{const e=document.querySelector(s);const r=e.getBoundingClientRect();return {top:Math.round(r.top+scrollY),h:Math.round(r.height),w:Math.round(r.width),left:Math.round(r.left)}}""", sel)
    info={}
    info['upTear']=box('.paper-tear.paper-tear-up')
    info['dwnTear']=box('body > .paper-tear:not(.paper-tear-up)')
    info['substrateVisual']=box('.feature.substrate .feature-visual')
    info['bandVisual']=box('.cb-visual')
    info['mmBefore']=pg.evaluate("()=>getComputedStyle(document.querySelector('#mm-feature .feature-visual'),'::before').transform")
    info['dwnMask']=pg.evaluate("()=>{const e=document.querySelectorAll('.paper-tear:not(.paper-tear-up) img');return e.length?getComputedStyle(e[0]).maskImage:'none'}")
    info['upMask']=pg.evaluate("()=>getComputedStyle(document.querySelector('.paper-tear-up img')).maskImage")
    info['subVisualBg']=pg.evaluate("()=>getComputedStyle(document.querySelector('.feature.substrate .feature-visual')).backgroundImage")
    print(info)
    # screenshots
    for name,sel in [('up','.paper-tear.paper-tear-up'),('down','body > .paper-tear:not(.paper-tear-up)'),('sub','.feature.substrate'),('band','.composure-band'),('mm','#mm-feature')]:
        try:
            pg.locator(sel).first.screenshot(path=f"temp/{OUT}_{name}.png")
        except Exception as e: print(name, e)
    b.close()
