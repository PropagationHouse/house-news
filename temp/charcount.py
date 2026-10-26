import re
p = r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news\composure\index.html"
h = open(p, encoding="utf-8").read()
b = h.split("<body",1)[1]
b = re.sub(r"<script.*?</script>", " ", b, flags=re.S)
b = re.sub(r"<style.*?</style>", " ", b, flags=re.S)
b = re.sub(r"<[^>]+>", " ", b)
b = re.sub(r"&[a-z]+;", " ", b)
b = re.sub(r"\s+", " ", b).strip()
print("body text chars:", len(b))
print("words:", len(b.split()))
