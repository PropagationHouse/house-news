from playwright.sync_api import sync_playwright
import os
OUT=r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp"
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":900})
    pg.goto("http://localhost:8099/composure/?cb=blue2",wait_until="networkidle")
    pg.wait_for_timeout(1200)
    pg.screenshot(path=os.path.join(OUT,"blue_full.png"),full_page=True)
    pg.screenshot(path=os.path.join(OUT,"blue_hero.png"))
    el=pg.query_selector("#rooms")
    if el: el.screenshot(path=os.path.join(OUT,"blue_rooms.png"))
    print("ok", pg.evaluate("document.body.scrollHeight"))
    b.close()
