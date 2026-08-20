import re
html = open('index.html', encoding='utf-8').read()
targets = ('#e8dcc8','#4ade80','#86efac','#fde68a','#fbbf24','#fdba74','#c4b5fd','#fca5a5','#a78bfa','#2dd4bf','#fb923c','#d1d5db','#9ca3af','#6b7280','#4b5563')
for m in re.finditer(r'<text[^>]*fill="([^"]+)"[^>]*>([^<]+)</text>', html):
    fill, txt = m.group(1), m.group(2).strip()
    if fill in targets:
        print(fill, '|', txt[:70])
