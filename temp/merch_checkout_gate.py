import io, os, json, re
R = r'C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news'
fails = []
def ck(name, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ') + name + (' ' + str(extra) if extra else ''))
    if not cond: fails.append(name)

# 1. api files exist
for f in ['api/checkout.js', 'api/finalize-order.js', 'api/printful-proxy.js', 'api/verify.js']:
    ck('exists ' + f, os.path.exists(os.path.join(R, f)))

# 2. checkout.js content
co = io.open(os.path.join(R, 'api/checkout.js'), encoding='utf-8').read()
ck('checkout: STRIPE_PRICE_HOODIE', 'STRIPE_PRICE_HOODIE' in co)
ck('checkout: STRIPE_PRICE_TEE', 'STRIPE_PRICE_TEE' in co)
ck('checkout: STRIPE_PRICE_BEANIE', 'STRIPE_PRICE_BEANIE' in co)
ck('checkout: success_url session', '{CHECKOUT_SESSION_ID}' in co)
ck('checkout: shipping_address_collection', 'shipping_address_collection' in co)
ck('checkout: no hardcoded price_', 'price_1' not in co)

# 3. finalize-order.js
fo = io.open(os.path.join(R, 'api/finalize-order.js'), encoding='utf-8').read()
ck('finalize: paid check', "payment_status !== 'paid'" in fo)
ck('finalize: status confirmed', "status: 'confirmed'" in fo)
ck('finalize: uses metadata', 'metadata.size' in fo)
ck('finalize: variant map', '5530' in fo and '20487' in fo)

# 4. shop-config.js
sc = io.open(os.path.join(R, 'shop/shop-config.js'), encoding='utf-8').read()
ck('config: soldOut false x3', sc.count('soldOut: false') == 3, sc.count('soldOut: false'))
ck('config: soldOut true gone', 'soldOut: true' not in sc)
ck('config: printfulId 146', 'printfulId: 146' in sc)
ck('config: printfulId 1592', 'printfulId: 1592' in sc)
ck('config: printfulId 809', 'printfulId: 809' in sc)
ck('config: prices 55/30/28', 'price: 55' in sc and 'price: 30' in sc and 'price: 28' in sc)

# 5. shop.js
sj = io.open(os.path.join(R, 'shop/shop.js'), encoding='utf-8').read()
ck('shop.js: calls /api/checkout', '/api/checkout' in sj)
ck('shop.js: posts printfulId', 'productId: p.printfulId' in sj)
ck('shop.js: old payment-link note gone', 'payment link' not in sj)
ck('shop.js: braces balanced', sj.count('{') == sj.count('}'), (sj.count('{'), sj.count('}')))

# 6. thanks page
th = io.open(os.path.join(R, 'shop/thanks.html'), encoding='utf-8').read()
ck('thanks.html exists + doctype', th.strip().startswith('<!DOCTYPE html>'))
ck('thanks.html closes html', th.rstrip().endswith('</html>'))
ck('thanks.html loads thanks.js', '/shop/thanks.js' in th)
tj = io.open(os.path.join(R, 'shop/thanks.js'), encoding='utf-8').read()
ck('thanks.js calls finalize-order', '/api/finalize-order' in tj)

# 7. vercel.json routes
vj = json.load(io.open(os.path.join(R, 'vercel.json'), encoding='utf-8'))
srcs = [r['source'] for r in vj['rewrites']]
ck('vercel: /shop/thanks route', '/shop/thanks' in srcs)
ck('vercel: 3 product routes', all(('/shop/' + s) in srcs for s in ['house-hoodie', 'daily-edition-tee', 'fisherman-beanie']))

# 8. css
css = io.open(os.path.join(R, 'shop/shop.css'), encoding='utf-8').read()
ck('css: .thanks block', '.thanks{' in css)
ck('css: #order-status', '#order-status{' in css)
ck('css: braces balanced', css.count('{') == css.count('}'), (css.count('{'), css.count('}')))

print('')
print('FAILS=' + str(len(fails)))
if fails: print('FAILED: ' + ', '.join(fails))
