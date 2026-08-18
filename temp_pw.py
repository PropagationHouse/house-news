from PIL import Image
import io, urllib.request

# Fetch the page and check the three tear images load
for path in ['assets/images/torn-drop-strip.png','assets/images/torn-up-strip.png','assets/images/torn-down-strip.png']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8777/{path}')
        data = r.read()
        im = Image.open(io.BytesIO(data))
        print(f'{path}: {len(data)} bytes, {im.size}, mode={im.mode}')
    except Exception as e:
        print(f'{path}: ERROR {e}')
