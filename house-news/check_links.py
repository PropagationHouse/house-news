import re, os, glob

base = os.getcwd()
files = glob.glob('**/*.html', recursive=True)

missing = []
for f in files:
    with open(f, encoding='utf-8', errors='replace') as fh:
        html = fh.read()
    for m in re.finditer(r'href="([^"]+)"', html):
        href = m.group(1)
        if href.startswith(('http', 'mailto:', 'tel:', 'data:', '#')):
            continue
        target = href.split('?')[0].split('#')[0]
        if not target:
            continue
        resolved = os.path.normpath(os.path.join(os.path.dirname(f), target))
        if not os.path.exists(resolved):
            missing.append((f, href, resolved))

if missing:
    print('MISSING TARGETS:')
    for f, h, r in sorted(set(missing)):
        print(f'  {f} -> {h}  (resolved: {r})')
else:
    print('ALL LOCAL LINKS RESOLVE OK')

# Also report any remaining placeholder hrefs
print('\nPLACEHOLDER HREFS (# or article.html):')
found = False
for f in files:
    with open(f, encoding='utf-8', errors='replace') as fh:
        html = fh.read()
    for m in re.finditer(r'href="(?:#|article\.html)"[^>]*>', html):
        print(f'  {f}: {m.group(0)}')
        found = True
if not found:
    print('  none')
