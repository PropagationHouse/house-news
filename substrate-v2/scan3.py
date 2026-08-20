html = open('index.html', encoding='utf-8').read()
for i, line in enumerate(html.split('\n'), 1):
    if 'terminal-bg' in line or 'diagram-bg' in line:
        print(i, line.strip()[:110])
