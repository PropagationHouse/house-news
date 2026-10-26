from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    bad=[]
    pg.on('response',lambda r: bad.append(str(r.status)+' '+r.url) if r.status>=400 else None)
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1500)
    print('BAD RESPONSES:', bad or 'none')
    imgs=pg.evaluate("()=>[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
    print('BROKEN IMGS:', imgs or 'none')
    print('img count:', pg.evaluate('document.images.length'))
    b.close()
