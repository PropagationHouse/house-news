from playwright.sync_api import sync_playwright
JS = """() => {
  const out=[];
  document.querySelectorAll('*').forEach(e=>{
    const cs=getComputedStyle(e);
    const bg=cs.backgroundColor;
    if(bg && bg!=='rgba(0, 0, 0, 0)'){
      const m=bg.match(/rgba?\\((\\d+), (\\d+), (\\d+)(?:, ([\\d.]+))?\\)/);
      if(m){
        const lum=(0.2126*+m[1]+0.7152*+m[2]+0.0722*+m[3])/255;
        if(lum<0.45){
          out.push((e.tagName+'.'+(e.className||'').toString().slice(0,60))+' | bg='+bg+' | lum='+lum.toFixed(2)+' | txt='+e.textContent.trim().slice(0,45).replace(/\\s+/g,' '));
        }
      }
    }
  });
  return out.join('\\n');
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1000)
    print(pg.evaluate(JS))
    b.close()
