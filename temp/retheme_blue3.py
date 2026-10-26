"""Decisive blue: paper reads as BLUE paper. Deeper, saturated. Page bg lighter blue."""
import re, os, shutil
HERE=r"C:\Users\Bl0ck\Desktop\desk\org\Propagation House Website Rebuild\house-news"
SRC=os.path.join(HERE,"composure","index.html")
BAK=os.path.join(HERE,"temp","composure_index_pre_blue3.html")
HEX={
 # page bg + light surfaces -> saturated light blue
 "#d6ecf7":"#c2e2f2",
 "#aed9ec":"#9fd0e8",
 "#8cc6e0":"#7cc0de",
 "#5aa8cc":"#4fa6cf",
 "#dceff8":"#cbe7f4",
 "#b4d8e8":"#a3d0e5",
 "#9ccbdf":"#8cc2da",
 "#7fb6d0":"#6fb0cf",
 "#63a3c2":"#57a0c4",
 "#4d91b3":"#4494ba",
}
with open(SRC,encoding="utf-8") as f: html=f.read()
shutil.copyfile(SRC,BAK)
def sub(m):
    tok="#"+m.group(1).lower(); return HEX.get(tok,m.group(0))
html,n=re.subn(r"#([0-9a-fA-F]{6})\b",sub,html)
with open(SRC,"w",encoding="utf-8") as f: f.write(html)
print("rewritten",n)
