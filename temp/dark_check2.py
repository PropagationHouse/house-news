from playwright.sync_api import sync_playwright
from PIL import Image
import collections
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1600)
    pg.screenshot(path='temp\\dark_full2.png',full_page=True)
    # check for any dark-on-dark remnants: find elements w/ low contrast text vs their painted bg
    JS = """() => {
      const bad=[];
      document.querySelectorAll('h1,h2,h3,p,li,span,a,figcaption').forEach(e=>{
        const cs=getComputedStyle(e);
        const t=e.textContent.trim();
        if(t.length<3) return;
        const c=cs.color.match(/[\\d.]+/g).map(Number);
        const lum=0.2126*c[0]+0.7152*c[1]+0.0722*c[2];
        if(lum<150) bad.push(e.tagName+'.'+String(e.className).slice(0,40)+' | '+cs.color+' | '+t.slice(0,40));
      });
      return bad.slice(0,25).join('\\n')||'NONE';
    }"""
    print(pg.evaluate(JS))
    print('--- logo ---')
    print(pg.evaluate("""()=>{const i=document.querySelector('nav img');return i?i.currentSrc+' '+i.naturalWidth:''}"""))
    b.close()
