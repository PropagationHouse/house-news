import io, json, urllib.request, sys
fails = []
def ck(name, cond, extra=''):
    print(('PASS ' if cond else 'FAIL ') + name + (' ' + str(extra) if extra else ''))
    if not cond: fails.append(name)

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        r = urllib.request.urlopen(req, timeout=45)
        return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')
    except Exception as e:
        return 0, str(e)

B = 'https://propagation.house'

# Shop index
st, body = get(B + '/shop')
ck('GET /shop 200', st == 200, st)
ck('shop index loads shop.js', '/shop/shop.js' in body)

# Product page
st, body = get(B + '/shop/house-hoodie')
ck('GET /shop/house-hoodie 200', st == 200, st)
ck('hoodie page loads shop.js', '/shop/shop.js' in body)

# thanks page
st, body = get(B + '/shop/thanks')
ck('GET /shop/thanks 200', st == 200, st)
ck('thanks has order-status', 'order-status' in body)
ck('thanks loads thanks.js', '/shop/thanks.js' in body)

# shop.js served + carries checkout call
st, body = get(B + '/shop/shop.js')
ck('GET /shop/shop.js 200', st == 200, st)
ck('shop.js calls /api/checkout', '/api/checkout' in body)
ck('shop.js has printfulId', 'printfulId' in body)

# config served + open
st, body = get(B + '/shop/shop-config.js')
ck('GET /shop/shop-config.js 200', st == 200, st)
ck('config: soldOut false x3', body.count('soldOut: false') == 3, body.count('soldOut: false'))

# thanks.js served
st, body = get(B + '/shop/thanks.js')
ck('GET /shop/thanks.js 200', st == 200, st)
ck('thanks.js calls finalize-order', '/api/finalize-order' in body)

# checkout endpoint exists (POST only -> GET should be 405)
st, body = get(B + '/api/checkout')
ck('GET /api/checkout = 405 (endpoint deployed)', st == 405, st)

print('')
print('FAILS=' + str(len(fails)))
if fails: print('FAILED: ' + ', '.join(fails))
