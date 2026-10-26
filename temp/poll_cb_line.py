import urllib.request, time, sys, datetime
URL = "https://www.propagation.house/"
NEW = ".composure-band .cb-visual{position:relative;"
OLD = "border-left:1px solid var(--rule);position:relative"
def log(m):
    line = "%s  %s" % (datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), m)
    print(line, flush=True)
log("poller start - waiting for commit cfae53c (composure band stray line removed) to go live")
for i in range(72):
    try:
        req = urllib.request.Request(URL, headers={"Cache-Control":"no-cache","User-Agent":"Mozilla/5.0"})
        r = urllib.request.urlopen(req, timeout=25)
        h = r.read().decode("utf-8", "replace")
        lm = r.headers.get("Last-Modified")
        new_ok = NEW in h
        old_ok = OLD in h
        log("pending  new=%s old=%s  LM=%s" % (new_ok, old_ok, lm))
        if new_ok and not old_ok:
            log("LIVE  composure band stray line gone | LM=%s" % lm)
            log("DONE"); sys.exit(0)
    except Exception as e:
        log("err %s" % e)
    time.sleep(600)
log("TIMEOUT after 12h"); sys.exit(1)
