import sys, json
P = "vercel.json"
t = open(P, "rb").read().decode("utf-8")
old = '    {\r\n      "source": "/composure/",\r\n      "destination": "/composure/index.html"\r\n    },'
new = ('    {\r\n      "source": "/composure/",\r\n      "destination": "/composure/index.html"\r\n    },\r\n'
       '    {\r\n      "source": "/composure/downloads",\r\n      "destination": "/composure/downloads.html"\r\n    },\r\n'
       '    {\r\n      "source": "/composure/downloads/",\r\n      "destination": "/composure/downloads.html"\r\n    },')
n = t.count(old)
if n != 1:
    print("ABORT: found", n); sys.exit(1)
t = t.replace(old, new)
open(P, "wb").write(t.encode("utf-8"))
d = json.loads(t)
print("ok - valid json,", len(d["rewrites"]), "rewrites")
for r in d["rewrites"]:
    if "composure" in r["source"]: print("  ", r["source"], "->", r["destination"])
