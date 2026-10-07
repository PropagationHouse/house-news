import io
p = r'C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news\shop\shop-config.js'
s = io.open(p, encoding='utf-8').read()
s = s.replace('soldOut: true', 'soldOut: false')
s = s.replace('fallbackNote: "Checkout opens soon"', 'fallbackNote: "Select a size"')
io.open(p, 'w', encoding='utf-8').write(s)
print('done')
print('soldOut:false count =', s.count('soldOut: false'))
print('fallbackNote select-size =', ('Select a size' in s))
