import re
h=open(r"composure\index.html",encoding="utf-8").read()
low=h.lower()
for t in ["ble ","scribe"]:
    for m in re.finditer(re.escape(t), low):
        s=max(0,m.start()-40); e=min(len(h),m.end()+40)
        print(repr(t), "->", repr(h[s:e].replace("\n"," ")))
