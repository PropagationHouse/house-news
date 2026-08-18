import io, os, re, json
root = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news"
# 1) JSON validity
aj = json.load(io.open(os.path.join(root, "house-news", "content", "articles.json"), encoding="utf-8"))
print("JSON OK, published:", len(aj["published"]))
# 2) Broken image refs in index/timeline/articles
html_files = [os.path.join(root, "house-news", "index.html"), os.path.join(root, "house-news", "timeline.html")] + [
    os.path.join(root, "house-news", "articles", f) for f in os.listdir(os.path.join(root, "house-news", "articles")) if f.endswith(".html")
]
img_re = re.compile(r'src="\.\./assets/images/([^"]+)"')
missing = []
for hp in html_files:
    t = io.open(hp, encoding="utf-8").read()
    for m in img_re.finditer(t):
        img = m.group(1)
        p = os.path.join(root, "house-news", "assets", "images", img)
        if not os.path.exists(p):
            missing.append((os.path.basename(hp), img))
print("missing images:", missing if missing else "NONE")
# 3) Article hrefs in index
href_re = re.compile(r'href="articles/([^"]+\.html)"')
bad_hrefs = []
for hp in html_files:
    t = io.open(hp, encoding="utf-8").read()
    for m in href_re.finditer(t):
        f = m.group(1)
        p = os.path.join(root, "house-news", "articles", f)
        if not os.path.exists(p):
            bad_hrefs.append((os.path.basename(hp), f))
print("bad article hrefs:", bad_hrefs if bad_hrefs else "NONE")
