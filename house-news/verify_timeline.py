import io, re, subprocess, sys, os
p = r"C:\Users\Bl0ck\AppData\Roaming\Substrate\workspace\projects\Propagation House Website Rebuild\house-news\house-news\timeline.html"
t = io.open(p, encoding="utf-8").read()
checks = [
    "id:'superman-leaps'",
    "id:'beijing-games'",
    "id:'san-mateo-permit'",
    '>21</div><div class="label"',
    'data-date="2026-08-17"',
    '  ];',
]
for k in checks:
    print(repr(k), "->", t.count(k))

# ── JS syntax check: extract the node-graph <script> and compile it with Node.
# This catches missing commas / unbalanced braces that would silently kill the graph.
m = re.search(r'<script>([\s\S]*?ARTICLES[\s\S]*?)</script>', t)
if not m:
    print("FAIL: node-graph script block not found")
    sys.exit(1)
js = m.group(1)
tmp = os.path.join(os.path.dirname(p), "_graph_check.js")
with io.open(tmp, "w", encoding="utf-8") as f:
    f.write(js)
r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True)
os.remove(tmp)
if r.returncode != 0:
    print("FAIL: node-graph JS syntax error:")
    print(r.stderr)
    sys.exit(1)
print("NODE-GRAPH JS: syntax OK")
