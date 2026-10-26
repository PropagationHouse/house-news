import re

P = 'composure/index.html'
lines = open(P, encoding='utf-8').read().split('\n')

needles = ['bg-[#8cc2da]/55', 'bg-[#0c86a8]/10', 'class="plate', 'room-card', 'mood-chip',
           'bg-[#0a5a7d]/[0.06]', 'text-[#0c86a8]', 'text-[#4d7285]', 'bg-[#8cc2da]']

for n in needles:
    print('=' * 70)
    print('### ' + n)
    for i, ln in enumerate(lines, 1):
        if n in ln:
            print('  [%d] %s' % (i, ln.strip()[:190]))
