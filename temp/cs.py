from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={'width':1280,'height':900},device_scale_factor=1)
    pg.goto('http://localhost:8099/composure/',wait_until='networkidle')
    pg.wait_for_timeout(1500)
    pg.screenshot(path='temp\\c_full.png',full_page=True)
    b.close()
im=Image.open('temp\\c_full.png'); print(im.size)
'W'|Out-Null
