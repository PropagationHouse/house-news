# -*- coding: utf-8 -*-
"""Probe OpenAI image API with gpt-image-1 (min body), log result."""
import json, os, urllib.request, urllib.error
from pathlib import Path

LOG = Path(__file__).with_name("hn89_imgprobe3.log")
log = LOG.open("w", encoding="utf-8")


def call(b):
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=json.dumps(b).encode(),
        method="POST",
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ["OPENAI_API_KEY"]})
    try:
        r = urllib.request.urlopen(req, timeout=240)
        d = json.load(r)
        item = d["data"][0]
        k = item.get("b64_json") or item.get("url") or ""
        log.write("OK model=%s len=%d head=%s\n" % (b["model"], len(k), k[:60]))
        if item.get("b64_json"):
            Path(__file__).with_name("hn89_probe_img.png").write_bytes(
                __import__("base64").b64decode(k))
            log.write("saved probe image\n")
    except urllib.error.HTTPError as e:
        log.write("ERR %s %d %s\n" % (b["model"], e.code, e.read().decode()[:300]))
    except Exception as e:
        log.write("EXC %s %r\n" % (b["model"], e))
    log.flush()


call({"model": "gpt-image-1", "prompt": "a plain grey square, flat illustration",
      "n": 1, "size": "1536x1024"})
log.close()
print("done")
