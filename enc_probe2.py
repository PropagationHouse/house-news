import io
p = "composure/index.html"
raw = open(p, "rb").read()
print("bytes:", len(raw))
print("has BOM:", raw[:3] == b"\xef\xbb\xbf")
try:
    t = raw.decode("utf-8")
    print("utf-8 decode OK, chars:", len(t))
except Exception as e:
    print("utf-8 FAIL", e)
    t = raw.decode("cp1252")
    print("cp1252 decode OK")
i = t.find("A Sonic Sketchbook")
print("sample:", repr(t[i-30:i+40]))
print("em dash count:", t.count("\u2014"))
print("CRLF:", raw.count(b"\r\n"), "LF:", raw.count(b"\n"))
