"""Rebuild the deep tear strips as REAL paper edges that blend into the field.

Goal (Michael, 13:19): a cleaner blend line between the torn paper edges and the
page field, reading like actual torn paper, tinted for this page.

Approach:
  - field lifted a touch toward the paper tone (see --ui-bg in index.html)
  - tear body ramps from the FIELD tone (flat end) up to the PAPER tone (ragged end),
    so the strip dissolves into the page instead of butting against it
  - the ragged lip carries a lit fiber highlight, modulated by the original paper
    texture, so the silhouette reads as a torn edge
"""
from PIL import Image
import numpy as np

FIELD = (10, 44, 56)     # #0a2c38 - lifted page field (was #06242c)
PAPER = (20, 66, 86)     # #144256 - the paper sheet tone
LIP   = (74, 142, 172)   # #4a8eac - lit fiber edge


def build(src, dst, up):
    im = Image.open(src).convert('RGBA')
    a = np.asarray(im).astype(float)
    alpha = a[..., 3]
    rgb = a[..., :3]
    g = (rgb @ np.array([0.2126, 0.7152, 0.0722])) / 255.0
    g = np.clip((g - g.min()) / max(1e-6, (g.max() - g.min())), 0, 1)
    h, w = alpha.shape

    y = np.arange(h) / (h - 1)
    if up:      # ragged lip at TOP, flat end at bottom
        edge = np.clip(1.0 - y / 0.42, 0, 1)     # 1 at lip -> 0 across body
        lip  = np.clip(1.0 - y / 0.10, 0, 1)     # tight highlight at the lip
    else:       # ragged lip at BOTTOM
        edge = np.clip((y - 0.58) / 0.42, 0, 1)
        lip  = np.clip((y - 0.90) / 0.10, 0, 1)

    edge = edge[:, None, None]
    lip  = lip[:, None, None]
    field = np.array(FIELD, float)[None, None, :]
    paper = np.array(PAPER, float)[None, None, :]
    lipc  = np.array(LIP, float)[None, None, :]

    col = field + edge * (paper - field)          # field -> paper ramp
    col = np.broadcast_to(col, (h, w, 3)).copy()
    col = col + lip * (lipc - col)                # lit fiber lip
    col = col * (0.90 + 0.20 * g)[..., None]      # keep the paper texture

    out = np.zeros((h, w, 4), np.uint8)
    out[..., :3] = np.clip(col, 0, 255).astype(np.uint8)
    out[..., 3] = alpha.astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(dst)
    print('->', dst, (w, h), 'field', FIELD, 'paper', PAPER, 'lip', LIP)


build('torn-up-strip-blue.png',   'torn-up-strip-deep.png',   up=True)
build('torn-down-strip-blue.png', 'torn-down-strip-deep.png', up=False)
