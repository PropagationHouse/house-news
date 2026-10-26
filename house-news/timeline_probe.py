import io, re
t = io.open('timeline.html', encoding='utf-8').read()
ids = re.findall(r"\{id:'([a-z0-9\-]+)'", t)
print('ARTICLES entries:', len(ids))
print('first 3:', ids[:3])
print('last 3:', ids[-3:])
print('total-count occurrences:', t.count('total-count'))
i = t.find('total-count')
print(repr(t[max(0,i-400):i+200]))
