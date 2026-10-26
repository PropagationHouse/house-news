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

# 1. desktop: kill the internal column rule on the composure band visual
rep(".composure-band .cb-visual{border-left:1px solid var(--rule);position:relative;",
    ".composure-band .cb-visual{position:relative;",
    1, "desktop cb-visual border-left removed")

# 2. mobile: kill the stacked-mode top rule too (same stray-line element)
rep(".composure-band .cb-visual{border-left:none;border-top:1px solid var(--rule);min-height:0;padding:2.7% 5.2%}",
    ".composure-band .cb-visual{min-height:0;padding:2.7% 5.2%}",
    1, "mobile cb-visual border-top removed")

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("\n".join(log))
print("---")
print("cb-visual border hits remaining:", s.count(".composure-band .cb-visual{border"))
print("braces:", s.count("{"), "/", s.count("}"))
print("ends html:", s.rstrip().endswith("</html>"))
