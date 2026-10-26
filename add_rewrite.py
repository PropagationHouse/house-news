import sys
P = "vercel.json"
raw = open(P, "rb").read()
t = raw.decode("utf-8")
old = '''    {
      "source": "/composure/",
      "destination": "/composure/index.html"
    },'''
new = '''    {
      "source": "/composure/",
      "destination": "/composure/index.html"
    },
    {
      "source": "/composure/downloads",
      "destination": "/composure/downloads.html"
    },
    {
      "source": "/composure/downloads/",
      "destination": "/composure/downloads.html"
    },'''
n = t.count(old)
if n != 1:
    print("ABORT: found", n); sys.exit(1)
t = t.replace(old, new)
open(P, "wb").write(t.encode("utf-8"))
print("ok vercel.json rewrite added")
