import io
p='index.html'
s=open(p,encoding='utf-8').read()

# 1. Issue number + date in masthead and footer
s = s.replace('Vol. III \u00b7 No. 52', 'Vol. III \u00b7 No. 53')
s = s.replace('Monday, August 17, 2026', 'Tuesday, August 18, 2026')
s = s.replace('Vol. III \u00b7 No. 52 \u00b7 August 17, 2026', 'Vol. III \u00b7 No. 53 \u00b7 August 18, 2026')

# Fallback if the middle-dot char is different
if 'No. 52' in s:
    s = s.replace('No. 52', 'No. 53')
if 'August 17, 2026' in s:
    s = s.replace('August 17, 2026', 'August 18, 2026')

# 2. Ticker: add two new headlines at the top of BOTH halves
new_items = [
    '<span>Nvidia backs OpenAI\u2019s Ohio campus with a $105B guarantee</span>',
    '<span>Stripe buys OpenRouter for $7B+ \u2014 the toll road changes hands</span>',
]
# First half: after the first <div class="ticker-track">
first_half_anchor = '<div class="ticker-track">\n'
idx = s.find(first_half_anchor)
if idx >= 0:
    insert_pos = idx + len(first_half_anchor)
    s = s[:insert_pos] + '\n'.join(new_items) + '\n' + s[insert_pos:]

# Second half: find the second occurrence of the first original item (after the first half)
item1 = '<span>Unitree'
occ = s.find(item1)
occ2 = s.find(item1, occ+1)
if occ2 >= 0:
    s = s[:occ2] + '\n'.join(new_items) + '\n' + s[occ2:]

open(p,'w',encoding='utf-8').write(s)
print('done')
print('No. 53 count:', s.count('No. 53'))
print('Aug 18 count:', s.count('August 18, 2026'))
print('ticker new item count:', s.count('Ohio campus with a $105B guarantee'))
print('ticker new item2 count:', s.count('toll road changes hands'))