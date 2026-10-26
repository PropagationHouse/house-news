import re,collections
src=open('composure/index.html',encoding='utf-8').read()
c=collections.Counter(re.findall(r'(?:text|bg|border|from|via|to)-\[#[0-9a-fA-F]{3,8}\](?:/\[?[\d.]+\]?)?|(?:text|bg|border)-(?:brand|paper|ink)-\d+(?:/[\[\]\d.]+)?|#[0-9a-fA-F]{6}|rgba?\([^)]*\)',src))
for k,v in c.most_common(): print(v,k)
