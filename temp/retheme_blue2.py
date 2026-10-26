"""Push saturation: page bg + paper should clearly read BLUE, not white-with-cast.
Second blue pass on top of the first."""
import re, os, shutil
HERE=r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news"
SRC=os.path.join(HERE,"composure","index.html")
BAK=os.path.join(HERE,"temp","composure_index_pre_blue2.html")

HEX={
 # light ramp -> more saturated blue
 "#e4f2f9":"#d6ecf7",
 "#c6e3f0":"#aed9ec",
 "#a4d1e5":"#8cc6e0",
 "#72b6d3":"#5aa8cc",
 "#eaf5fa":"#dceff8",
 "#cfe6ef":"#b4d8e8",
 "#b9d9e7":"#9ccbdf",
 "#9cc7da":"#7fb6d0",
 "#7fb4cb":"#63a3c2",
 "#63a1bc":"#4d91b3",
 # keep dark ramp as-is (already matches UI)
}
with open(SRC,encoding="utf-8") as f: html=f.read()
shutil.copyfile(SRC,BAK)
def sub(m):
    tok="#"+m.group(1).lower(); return HEX.get(tok,m.group(0))
html,n=re.subn(r"#([0-9a-fA-F]{6})\b",sub,html)
with open(SRC,"w",encoding="utf-8") as f: f.write(html)
print("rewritten",n)
