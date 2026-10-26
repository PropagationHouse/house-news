from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900})
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1600)
    pg.screenshot(path='temp\\dark_full3.png',full_page=True)
    b.close()
print('shot ok')
