import re
lines = open('index.html', encoding='utf-8', errors='replace').read().split('\n')
print('---SECTIONS---')
for i, l in enumerate(lines, 1):
    s = l.strip()
    if '<section' in s:
        m = re.search(r'class="([^"]*)"', s)
        cls = m.group(1) if m else ''
        print(f'{i:5}: {s[:160]}')
print('---TEARS---')
for i, l in enumerate(lines, 1):
    if 'paper-tear' in l and 'img src' in l:
        print(f'{i:5}: {l.strip()[:120]}')