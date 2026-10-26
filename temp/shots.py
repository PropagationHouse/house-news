from playwright.sync_api import sync_playwright
import pathlib
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(1800)
    for sel,name in [(".feature.substrate","substrate"),(".composure-band","composure"),("#mm-feature","walmart"),("#un-feature","un")]:
        el = pg.query_selector(sel)
        if el:
            el.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
            el.screenshot(path="temp/shot_%s.png"%name)
            print(name,"ok")
    b.close()
