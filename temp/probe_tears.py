import json, sys
from playwright.sync_api import sync_playwright
URL="file:///C:/Users/Bl0ck/Desktop/desk/org/Propagation%20House%20Website%20Rebuild/house-news/index.html"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(URL, wait_until="load")
    pg.wait_for_timeout(1500)
    res=pg.evaluate("""()=>{
      const q=s=>document.querySelector(s);
      const box=e=>{const r=e.getBoundingClientRect();return {top:Math.round(r.top+scrollY),h:Math.round(r.height),w:Math.round(r.width)}};
      const tears=[...document.querySelectorAll('.paper-tear')].map((e,i)=>({i,cls:e.className,img:e.querySelector('img').getAttribute('src'),...box(e)}));
      const cs=s=>{const e=q(s);const c=getComputedStyle(e);return {mask:c.maskImage,webkit:c.webkitMaskImage,transform:c.transform,bg:c.backgroundColor}};
      return {
        tears,
        tearUp:cs('.paper-tear-up img'),
        tearDown:cs('.paper-tear:not(.paper-tear-up) img'),
        band:box(q('.composure-band')),
        bandVisual:cs('.cb-visual'),
        bandBefore:getComputedStyle(q('.cb-visual'),'::before').transform,
        substrateVisual:{...box(q('.feature.substrate .feature-visual')),bg:getComputedStyle(q('.feature.substrate .feature-visual')).backgroundColor,mh:getComputedStyle(q('.feature.substrate .feature-visual')).minHeight},
        substrateImg:box(q('.feature.substrate .feature-visual img')),
        mmBefore:getComputedStyle(q('#mm-feature .feature-visual'),'::before').transform,
        unBefore:getComputedStyle(q('#un-feature .feature-visual'),'::before').transform,
        bridgeBefore:getComputedStyle(q('#the-bridge .feature-visual'),'::before').transform
      };
    }""")
    print(json.dumps(res,indent=1))
    b.close()
