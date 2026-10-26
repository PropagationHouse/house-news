import re,os
html=open(r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp\cp_build.html",encoding="utf-8").read()
print("=== image srcs ===")
srcs=re.findall(r'src="([^"]+)"',html)
for s in sorted(set(srcs)):
    if s.startswith("data:"): print("  OK  (inline svg)"); continue
    if s.startswith("http"): print("  EXT ",s); continue
    path=os.path.normpath(os.path.join("composure",s))
    print(("  OK  " if os.path.exists(path) else "  MISS"),s,"->",path)
print()
print("=== internal anchors ===")
ids=set(re.findall(r'id="([^"]+)"',html))
hrefs=set(re.findall(r'href="#([^"]+)"',html))
for h in sorted(hrefs):
    print(("  OK  " if h in ids else "  MISS"),"#"+h)
print()
print("=== internal page links ===")
for h in sorted(set(re.findall(r'href="([^"#][^"]*)"',html))):
    if h.startswith("http") or h.startswith("mailto"): continue
    path=os.path.normpath(os.path.join("composure",h))
    print(("  OK  " if os.path.exists(path) else "  MISS"),h,"->",path)
