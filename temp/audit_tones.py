import re, collections, os

P = 'composure/index.html'
h = open(P, encoding='utf-8').read()
body = h[h.index('<body'):]

cls = re.findall(r'class="([^"]*)"', body)
tok = collections.Counter()
for c in cls:
    for t in c.split():
        if any(k in t for k in ['ink', 'paper', 'brand', '#']):
            tok[t] += 1
print('=== class tokens in body ===')
for t, c in sorted(tok.items()):
    print('%3d  %s' % (c, t))

print()
print('=== custom CSS rules with a background ===')
for m in re.finditer(r'([^\n{}]+)\{([^}]*)\}', h):
    sel, dec = m.group(1).strip(), m.group(2)
    if 'background' in dec or 'color' in dec:
        print('%-46s %s' % (sel[:46], dec.strip()[:120]))
