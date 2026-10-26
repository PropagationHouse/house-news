from playwright.sync_api import sync_playwright
from PIL import Image
import pathlib
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(1500)
    up = pg.evaluate("()=>{const e=document.querySelector('.paper-tear-up');const r=e.getBoundingClientRect();return {top:r.top+window.scrollY,h:r.height};}")
    dn = pg.evaluate("()=>{const e=document.querySelector('.paper-tear:not(.paper-tear-up)');const r=e.getBoundingClientRect();return {top:r.top+window.scrollY,h:r.height};}")
    print("up",up,"dn",dn)
    pg.screenshot(path="temp/full_after.png", full_page=True)
    b.close()
im = Image.open("temp/full_after.png"); print("full", im.size)
# crop up region: 160 above tear top to 160 below
def crop(top, name):
    y0=max(0,int(top)-170); y1=min(im.size[1], int(top)+250)
    im.crop((0,y0,im.size[0],y1)).save(name)
crop(up["top"],"temp/tear_up_after.png")
crop(dn["top"],"temp/tear_down_after.png")
print("done")
