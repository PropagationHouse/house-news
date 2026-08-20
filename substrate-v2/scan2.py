import re
html = open('index.html', encoding='utf-8').read()
for i, line in enumerate(html.split('\n'), 1):
    if 'terminal-bg rounded-3xl border border-white/10' in line:
        print(i, line.strip()[:120])
