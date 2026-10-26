from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np, pathlib
url = pathlib.Path("index.html").resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width":1440,"height":1000})
    pg.goto(url, wait_until="load"); pg.wait_for_timeout(1500)
    up = pg.evaluate("()=>{const e=document.querySelector('.paper-tear-up');const r=e.getBoundingClientRect();return {top:r.top+window.scrollY,h:r.height};}")
    dn = pg.evaluate("()=>{const e=document.querySelector('.paper-tear:not(.paper-tear-up)');const r=e.getBoundingClientRect();return {top:r.top+window.scrollY,h:r.height};}")
    pg.screenshot(path="temp/full_after.png", full_page=True)
    b.close()
im = np.asarray(Image.open("temp/full_after.png").convert("RGB")).astype(float)
prof = im.mean(axis=(1,2))
def report(label, top, h):
    t=int(top); H=int(h)
    # look at 40px above tear top through tear
    a=max(0,t-40); z=min(len(prof), t+H)
    seg = prof[a:z]
    d = np.abs(np.diff(seg))
    print("==",label,"tear top",t,"h",H)
    print("   max row jump in [top-40, top+h]:", round(d.max(),2), "at offset", int(d.argmax()), "(0=40px above tear)")
    # sample brightness at tear top boundary
    print("   brightness at top-3..top+3:", [round(x,1) for x in prof[t-3:t+4]])
report("UP", up["top"], up["h"])
report("DOWN", dn["top"], dn["h"])
