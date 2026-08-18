import io
p = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news\house-news\timeline.html"
t = io.open(p, encoding="utf-8").read()
checks = [
    "id:'superman-leaps'",
    "id:'beijing-games'",
    "id:'san-mateo-permit'",
    '>21</div><div class="label"',
    'data-date="2026-08-17"',
    '  ];',
]
for k in checks:
    print(repr(k), "->", t.count(k))
