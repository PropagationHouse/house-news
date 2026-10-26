from playwright.sync_api import sync_playwright
import json
JS = """() => {
  const out=[];
  const sel=['body','header','main','section','.card-hover','.room-row','.title-paper-wrap','.title-paper-wrap h1','.title-paper-wrap h2','h1','h2','h3','p','.gradient-text','.bg-brand-500\\\\/10'];
  for(const s of sel){
    const els=[...document.querySelectorAll(s)].slice(0,5);
    els.forEach((e,i)=>{
      const cs=getComputedStyle(e);
      out.push(s+'#'+i+' bg='+cs.backgroundColor+' color='+cs.color+' txt='+e.textContent.trim().slice(0,50).replace(/\\s+/g,' '));
    });
  }
  return out.join('\\n');
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1000)
    print(pg.evaluate(JS))
    b.close()
