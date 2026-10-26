import re
h=open("composure/index.html",encoding="utf-8").read()
cls=set()
for m in re.finditer(r'class="([^"]*)"', h):
    for c in m.group(1).split():
        if re.search(r'(brand|paper|ink|#[0-9a-f]{6})', c):
            cls.add(c)
for c in sorted(cls):
    print(c)
