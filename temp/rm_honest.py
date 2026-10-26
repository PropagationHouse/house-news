import io, sys
p = r"composure/index.html"
s = io.open(p, encoding="utf-8").read()
orig = s

# 1) Remove the HONEST NOTES section block (comment -> closing </section>) plus the
#    trailing tear-down divider that followed it, leaving the tear-up divider before CTA.
start = s.index("    <!-- ==================== HONEST NOTES ==================== -->")
end = s.index("    <!-- ==================== CTA ==================== -->")
removed = s[start:end]
s = s[:start] + s[end:]

# 2) Remove the now-dead .honest-note CSS rule + its comment header.
css_old = "        /* HONEST NOTES */\n        .honest-note { border-left:3px solid rgba(179,64,47,0.55); padding-left:18px; }\n"
assert css_old in s, "CSS block not found"
s = s.replace(css_old, "")

io.open(p, "w", encoding="utf-8", newline="").write(s)
print("removed chars:", len(orig)-len(s))
print("removed lines:", removed.count("\n"))
