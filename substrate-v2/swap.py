html = open('index.html', encoding='utf-8').read()
# Only replace within diagram panels (after line 950 architecture section)
lines = html.split('\n')
count = 0
for i, line in enumerate(lines):
    if 'terminal-bg rounded-3xl border border-white/10 p-6 md:p-10 glow overflow-x-auto' in line and i+1 >= 976:
        lines[i] = line.replace('terminal-bg rounded-3xl border border-white/10', 'diagram-bg rounded-3xl')
        count += 1
open('index.html','w',encoding='utf-8').write('\n'.join(lines))
print('replaced', count)
