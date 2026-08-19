import io, re, os
from datetime import datetime
from email.utils import format_datetime

files = [f for f in os.listdir('articles') if f.endswith('.html') and f != 'test.html']
files.sort()

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

items = []
for fn in files:
    s = io.open(os.path.join('articles', fn), encoding='utf-8').read()
    tm = re.search(r'<title>([^<]+)</title>', s)
    title = re.sub(r'\s*[\u2013\u2014-]\s*(house|SIGNAL)\s*$', '', tm.group(1)) if tm else fn
    dm = re.search(r'class="dek">(.*?)</p>', s, re.S)
    dek = re.sub(r'<[^>]+>', '', dm.group(1)) if dm else ''
    dtm = re.search(r'(\w+ \d{1,2}, \d{4})', s)
    pub = ''
    if dtm:
        d = datetime.strptime(dtm.group(1), '%B %d, %Y')
        pub = format_datetime(d)
    url = 'https://www.propagation.house/house-news/articles/' + fn
    items.append((pub, title, dek, url))

items.sort(key=lambda x: x[0], reverse=True)

out = []
out.append('<?xml version="1.0" encoding="UTF-8"?>')
out.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
out.append('<channel>')
out.append('<title>house \u2014 Dispatches from the Edge of Culture, Technology &amp; Design</title>')
out.append('<link>https://www.propagation.house/house-news/</link>')
out.append('<description>Dispatches from Propagation House. What the machines are becoming \u2014 and what it means for the people who build, fund, and regulate them.</description>')
out.append('<language>en-us</language>')
out.append('<atom:link href="https://www.propagation.house/house-news/feed.xml" rel="self" type="application/rss+xml"/>')
for pub, title, dek, url in items:
    out.append('<item>')
    out.append('<title>%s</title>' % esc(title))
    out.append('<link>%s</link>' % url)
    out.append('<guid isPermaLink="true">%s</guid>' % url)
    if pub:
        out.append('<pubDate>%s</pubDate>' % pub)
    out.append('<description>%s</description>' % esc(dek))
    out.append('</item>')
out.append('</channel>')
out.append('</rss>')

io.open('feed.xml', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('feed.xml rebuilt with %d items' % len(items))
for pub, title, dek, url in items[:3]:
    print('-', title)

