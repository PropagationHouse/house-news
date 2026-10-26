import sys, json
from playwright.sync_api import sync_playwright
OUT=sys.argv[1]
URL="file:///C:/Users/Bl0ck/Desktop/desk/org/Propagation%20House%20Website%20Rebuild/house-news/index.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":1100})
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(1800)
    info=pg.evaluate("""()=>{
      const box=s=>{const e=document.querySelector(s); if(!e) return null; const r=e.getBoundingClientRect(); return {top:Math.round(r.top+scrollY),h:Math.round(r.height),w:Math.round(r.width),left:Math.round(r.left)}};
      const tears=[...document.querySelectorAll('.paper-tear')].map(e=>({cls:e.className,src:e.querySelector('img').getAttribute('src'),r:(()=>{const b=e.getBoundingClientRect();return {top:Math.round(b.top+scrollY),h:Math.round(b.height)}})()}));
      const gb=(s,ps)=>{const e=document.querySelector(s); if(!e) return null; const c=getComputedStyle(e,ps); return {transform:c.transform, bg:c.backgroundImage, mask:c.maskImage, box:c.boxShadow}};
      const img=(s)=>{const e=document.querySelector(s); if(!e) return null; const c=getComputedStyle(e); const r=e.getBoundingClientRect(); const n={w:e.naturalWidth,h:e.naturalHeight}; return {rect:{w:Math.round(r.width),h:Math.round(r.height)}, nat:n, objfit:c.objectFit, pos:c.position, shadow:c.boxShadow, z:c.zIndex}};
      return {tears, upTear:box('.paper-tear-up'), dwnTear:box('.paper-tear:not(.paper-tear-up)'),
        upMask:gb('.paper-tear-up img'), dwnMask:gb('.paper-tear:not(.paper-tear-up) img'),
        subVis:box('.feature.substrate .feature-visual'), subVisCS:gb('.feature.substrate .feature-visual'),
        subVisBefore:gb('.feature.substrate .feature-visual','::before'), subImg:img('.feature.substrate .feature-visual img'),
        cbVis:box('.cb-visual'), cbBefore:gb('.cb-visual','::before'), cbImg:img('.cb-visual img'),
        mmBefore:gb('#mm-feature .feature-visual','::before'), mmImg:img('#mm-feature .feature-visual img')};
    }""")
    print(json.dumps(info,indent=1))
    for name,sel in [('up','.paper-tear-up'),('down','.paper-tear:not(.paper-tear-up)'),('sub','#products .feature.substrate'),('band','.composure-band'),('mm','#mm-feature')]:
        try: pg.locator(sel).first.screenshot(path=f"temp/{OUT}_{name}.png")
        except Exception as e: print("shot fail",name,e)
    b.close()
