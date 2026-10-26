from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    pg=b.new_page(viewport={"width":1440,"height":900})
    errs=[]
    pg.on("console",lambda m: errs.append(m.text) if m.type=="error" else None)
    pg.on("requestfailed",lambda r: errs.append("REQFAIL "+r.url))
    pg.goto("http://localhost:8099/composure/?cb=v1",wait_until="networkidle")
    pg.wait_for_timeout(1000)
    # broken images
    broken=pg.evaluate("Array.from(document.images).filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src)")
    # any warm/reddish computed colors
    warm=pg.evaluate("""() => {
      const out=[];
      document.querySelectorAll('*').forEach(el=>{
        const s=getComputedStyle(el);
        ['backgroundColor','color','borderTopColor'].forEach(k=>{
          const v=s[k]; const m=v.match(/rgba?\\((\\d+),\\s*(\\d+),\\s*(\\d+)/);
          if(m){const r=+m[1],g=+m[2],bl=+m[3]; if(r>bl+15 && r>60) out.push(k+':'+v);}
        });
      });
      return [...new Set(out)].slice(0,10);
    }""")
    print("errors:", errs if errs else "none")
    print("broken imgs:", broken if broken else "none")
    print("warm colors:", warm if warm else "none")
    b.close()
