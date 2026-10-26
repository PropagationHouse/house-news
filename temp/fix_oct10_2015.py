# -*- coding: utf-8 -*-
import io
P = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\index.html"
s = io.open(P, encoding="utf-8", newline="").read()
log = []

def rep(old, new, expect, label):
    global s
    n = s.count(old)
    if n != expect:
        log.append("FAIL %s: found %d expected %d" % (label, n, expect)); return
    s = s.replace(old, new)
    log.append("OK   %s (%d)" % (label, n))

# --- 1. PAPER SHEETS: kill the rotation (mm, un, bridge, composure band) ---
rep("transform:rotate(-1.2deg)", "transform:none", 3, "sheet rot -1.2 -> none")
rep("transform:rotate(1.2deg)",  "transform:none", 1, "sheet rot +1.2 -> none")

# --- 2. SUBSTRATE: put the flagship image on the same house paper sheet ---
old252 = '.feature.substrate .feature-visual{min-height:0;float:right;width:47%;max-width:520px;margin:8px 0 16px 40px;background:linear-gradient(135deg,#0f1108,#1a1d12 55%,#4b5320);border-left:1px solid var(--rule)} /* wrap: image right, text flows around */'
new252 = ('.feature.substrate .feature-visual{min-height:0;float:right;width:47%;max-width:520px;margin:8px 0 16px 40px;'
          'background:transparent;border-left:none;position:relative;overflow:visible;padding:2.7% 5.2%;isolation:isolate}'
          ' /* wrap: image right, text flows around - image sits on the house paper sheet */\n'
          '.feature.substrate .feature-visual::before{content:"";position:absolute;inset:0;'
          'background:url("assets/images/paper-sheet-fill-2x.jpg?v=1") center/cover no-repeat;transform:none;z-index:0;'
          'box-shadow:0 14px 34px rgba(18,20,10,.15)}\n'
          '.feature.substrate .feature-visual::after{content:none}')
rep(old252, new252, 1, "substrate visual -> paper sheet + ::before")

old254 = '.feature.substrate .feature-visual img{position:relative;inset:auto;width:100%;height:auto;display:block}'
new254 = '.feature.substrate .feature-visual img{position:relative;inset:auto;width:100%;height:auto;display:block;z-index:1;object-fit:initial;box-shadow:0 6px 18px rgba(26,29,18,.14)}'
rep(old254, new254, 1, "substrate img z-index + shadow")

# --- 3. TORN PAPER DIVIDER (bottom / down-tear): clean gradient blend like the up-tear ---
old114 = '.paper-tear.paper-tear-up img{-webkit-mask-image:linear-gradient(to bottom,#000 52%,transparent 100%);mask-image:linear-gradient(to bottom,#000 52%,transparent 100%)}'
new114 = (old114 + '\n'
          '.paper-tear:not(.paper-tear-up) img{-webkit-mask-image:linear-gradient(to top,#000 52%,transparent 100%);'
          'mask-image:linear-gradient(to top,#000 52%,transparent 100%)}')
rep(old114, new114, 1, "down-tear gradient blend")

io.open(P, "w", encoding="utf-8", newline="").write(s)
for l in log: print(l)
print("BYTES", len(s))
