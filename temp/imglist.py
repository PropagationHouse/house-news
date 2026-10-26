import re
h=open("composure/index.html",encoding="utf-8").read()
# list every img with a bit of surrounding context, in order
for m in re.finditer(r'<img[^>]*src="([^"]+)"[^>]*>', h):
    src=m.group(1)
    # find nearest preceding section id
    pre=h[:m.start()]
    ids=re.findall(r'id="([a-z]+)"', pre)
    sec=ids[-1] if ids else "?"
    print(sec.ljust(14), src.split("/")[-1])
