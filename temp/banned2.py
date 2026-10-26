import re
h=open(r"composure\index.html",encoding="utf-8").read().lower()
banned=["bluetooth","ble ","physical model","thirteen rooms","websocket","json-rpc","ppq","mpe","n-api","portaudio","localhost:9473","9473","19319","basic pitch","five persistent","est. 2020","scribe","always listening","http fallback","oscillator bank","2,226","22.05"]
hits=[b for b in banned if b in h]
print("banned hits:", hits if hits else "NONE")
print("total chars:", len(h))
