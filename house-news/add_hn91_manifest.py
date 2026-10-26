# -*- coding: utf-8 -*-
import io
p = 'gen_images.py'
t = io.open(p, encoding='utf-8').read()
anchor = '    # ---------- NO. 90 (Oct 15, 2026) ----------\n'
assert anchor in t, 'anchor missing'
new = '''    # ---------- NO. 91 (Oct 16, 2026) ----------
    {"filename": "ftc-civil-demands-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a federal agency conference room, two thick bound document volumes stacked at each end of a long polished table, an empty brass nameplate holder at the head",
     "place": "an institutional federal agency conference room with tall windows and plain wall panelling",
     "camera": "straight on from the doorway at standing height, candid documentary distance, nobody in frame",
     "light": "cool overhead light pooled on the table surface, thin pale daylight through the tall windows behind",
     "scale_anchor": "the nameplate holder and the width of the table make the bound volumes scale obvious.",
     "lens": "35mm f/2.8 prime, 1/60s"},
    {"filename": "anthropic-q3-offering-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "an empty investment-bank boardroom at dusk, a single printed quarterly earnings sheet left face-up at the head of a long table, city towers dimming behind the glass",
     "place": "a high-rise investment-bank boardroom with floor-to-ceiling glass and a leather chair row",
     "camera": "from the far end of the table at standing height, candid documentary distance, nobody in frame",
     "light": "failing dusk light from the windows with a low warm downlight pooled on the printed sheet",
     "scale_anchor": "the chair row and table width make the single sheet of paper scale obvious.",
     "lens": "28mm f/4 prime, 1/50s"},
    {"filename": "frontier-distillation-pact-hero.jpg", "aspect_ratio": "16:9", "lane": "b",
     "subject": "a dim security operations room, a wall of monitors showing pale traffic graphs, a single printed incident report left on the desk beneath them, empty chair pushed back",
     "place": "a small security operations centre with a monitor wall and a single analyst desk",
     "camera": "from behind the desk chair at standing height looking toward the monitor wall, candid documentary distance, nobody in frame",
     "light": "the monitors as the main light source with a faint overhead wash, the room otherwise dim",
     "scale_anchor": "the desk chair and keyboard make the monitor wall scale obvious.",
     "lens": "24mm f/4 prime, 1/40s"},
'''
t = t.replace(anchor, new + anchor, 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('inserted, new len', len(t))
