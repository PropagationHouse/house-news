import re
html=open(r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\temp\cp_build.html",encoding="utf-8").read()
print("=== BANNED / STALE PHRASE SCAN ===")
banned={
 "physical-model":0,"not samples":0,"Always Listening":0,"always-listening":0,
 "thirteen rooms":0,"Thirteen rooms":0,"Est. 2020":0,"Five persistent":0,"five channels":0,
 "second-brain":0,"second brain":0,"Bluetooth MIDI":0,"vault path":0,
 "Muse":0,"second act":0,"boasts":0,"world-class":0,"cutting-edge":0,"seamlessly":0,
 "revolutionary":0,"game-changing":0,"unleash":0,"empower":0,"elevate":0,
}
low=html.lower()
for k in banned:
    n=low.count(k.lower())
    print(f"  {'OK ' if n==0 else 'HIT'} {k}: {n}")
print()
print("=== real app terms present ===")
for k in ["sixteen role-labeled","16 channels","Drums, Bass, Chords, Melody","modify_playback","9473",
          "24 PPQ","Basic Pitch","22.05 kHz","2226" ,"2,226","N-API","PortAudio","Lyria","Chladni",
          "fourteen","eleven","Est. 2013","no mockups","nothing is uploaded","Capacitor","MPE","19319",
          "fourteen moods","Dreamlike"]:
    print(f"  {'OK ' if k.lower() in low else 'MISS'} {k}")
