import io, json, os, urllib.request
# Read the Printful key from the repo .env.local
env_path = r'C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news\.env.local'
key = None
if os.path.exists(env_path):
    for line in io.open(env_path, encoding='utf-8'):
        line = line.strip()
        if line.startswith('PRINTFUL_API_KEY='):
            key = line.split('=', 1)[1].strip().strip('"').strip("'")
print('key found:', bool(key), 'prefix:', key[:8] if key else None)

def get(path):
    req = urllib.request.Request('https://api.printful.com' + path,
        headers={'Authorization': 'Bearer ' + key})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=45))
        return d
    except Exception as e:
        return {'_error': str(e)}

# Store info
st = get('/store')
print('store:', json.dumps(st.get('result', st), default=str)[:300] if '_error' not in st else st['_error'])

# Products in store
pr = get('/store/products')
if '_error' in pr:
    print('products ERR:', pr['_error'])
else:
    items = pr.get('result', [])
    print('store products count:', len(items))
    for it in items:
        vid = it.get('id')
        name = it.get('name')
        variants = it.get('variants', [])
        print(' ', vid, '|', name, '| variants:', len(variants))
