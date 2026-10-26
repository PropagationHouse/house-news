from playwright.sync_api import sync_playwright
JS = """() => {
  const out=[];
  const grab=(sel,n)=>{[...document.querySelectorAll(sel)].slice(0,n).forEach((e,i)=>{
    const cs=getComputedStyle(e);
    out.push(sel+'#'+i+' bg='+cs.backgroundColor+' color='+cs.color+' txt='+e.textContent.trim().slice(0,44).replace(/\\s+/g,' '));
  });};
  grab('body',1); grab('nav',1); grab('.card-hover',2); grab('.room-card',2); grab('.plate',2);
  grab('h2',4); grab('p',4); grab('.room-row p',2); grab('.mood-chip',1); grab('.hero-lede',1);
  return out.join('\\n');
}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1500)
    print(pg.evaluate(JS))
    pg.screenshot(path='temp\\dark_full.png',full_page=True)
    b.close()
