from playwright.sync_api import sync_playwright
JS = """() => {
  const out=[];
  document.querySelectorAll('*').forEach(e=>{
    const cs=getComputedStyle(e);
    const bg=cs.backgroundColor;
    const m=bg.match(/rgba?\\((\\d+), (\\d+), (\\d+)(?:, ([\\d.]+))?\\)/);
    if(m && (m[4]===undefined||+m[4]>0.3)){
      const lum=(0.2126*+m[1]+0.7152*+m[2]+0.0722*+m[3])/255;
      if(lum>0.5) out.push(e.tagName+'.'+String(e.className).slice(0,50)+' | '+bg+' | '+e.textContent.trim().slice(0,30));
    }
  });
  return out.slice(0,20).join('\\n')||'NO LIGHT SURFACES';
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1400)
    print(pg.evaluate(JS))
    b.close()
