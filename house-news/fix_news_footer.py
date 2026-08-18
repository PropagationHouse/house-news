import io

p = 'index.html'
s = io.open(p, encoding='utf-8').read()

# --- Sections footer: category links -> timeline ---
s = s.replace('<ul><li><a href="#">Technology</a></li><li><a href="#">Design</a></li><li><a href="#">Culture</a></li><li><a href="#">Business</a></li><li><a href="#">Ideas</a></li></ul>',
              '<ul><li><a href="timeline.html">Technology</a></li><li><a href="timeline.html">Design</a></li><li><a href="timeline.html">Culture</a></li><li><a href="timeline.html">Business</a></li><li><a href="timeline.html">Ideas</a></li></ul>')

# --- Follow footer: wire real links ---
s = s.replace('<ul><li><a href="#">Newsletter</a></li><li><a href="#">RSS</a></li><li><a href="#">X / Twitter</a></li><li><a href="#">GitHub</a></li></ul>',
              '<ul><li><a href="subscribe.html">Newsletter</a></li><li><a href="feed.xml">RSS</a></li><li><a href="https://github.com/PropagationHouse/house-news">GitHub</a></li></ul>')

io.open(p, 'w', encoding='utf-8').write(s)
print("DONE news footer")
