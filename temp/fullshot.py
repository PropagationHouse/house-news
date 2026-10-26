import sys
from playwright.sync_api import sync_playwright
URL="file:///C:/Users/Bl0ck/Desktop/desk/org/Propagation%20House%20Website%20Rebuild/house-news/index.html"
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":1440,"height":1200})
    pg.goto(URL, wait_until="load"); pg.wait_for_timeout(2000)
    pg.screenshot(path="temp/full_before.png", full_page=True, animations="disabled")
    pg.screenshot(path="temp/mast_before.png", clip={"x":0,"y":5250,"width":1440,"height":330})
    pg.screenshot(path="temp/lp_before.png", clip={"x":0,"y":3000,"width":1440,"height":330})
    b.close()
print("ok")
