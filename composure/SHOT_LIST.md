# Composure — Screenshot Shot List

**Purpose:** replace every illustrated placeholder on the Composure article + subpage with real captures from the running app.

**Naming:** save into `composure/shots/` using the exact filenames below. Don't crop tight — leave the full window frame visible; I'll crop and frame in CSS. Capture at native resolution (Retina/1440p+ ideal). PNG is fine, I'll convert.

**One rule:** the app UI is dark. The house paper is cream. That contrast is good — don't lighten or restyle anything for the shots. Capture what's actually on screen.

---

## ARTICLE — 4 slots
File: `house-news/articles/composure.html`
Currently: AI-rendered illustrations (Lane A style). All four get replaced.

### 1. `composure-hero.jpg` — 16:9 (target 1824x1024+)
**The one image that says what this is.**
Full desktop app window, maximized. Sidebar visible on the left, Scribe showing a captured session in the Timeline. If a session with real note content is on screen, better. No menus open, no dialogs, no cursor parked over a tooltip.

### 2. `composure-fig0.jpg` — 4:3
**Channels, not tracks — the proof.**
The channel map view showing all sixteen channels with their current role labels. This is the single most important correction to the old copy: the app has **16 addressable channels**, not five. Get the role labels legible.

### 3. `composure-fig1.jpg` — 4:3
**The agent at work — the collaborator pillar.**
The embedded copilot (or Substrate's chat) mid-conversation, with the instruction text visible AND the resulting change on screen. Best version: a plain-English ask ("make it darker", "transpose the bass") next to the channel map or timeline showing that only one voice moved. This is the shot that proves it's not a chatbot bolted on.

### 4. `composure-fig2.jpg` — full-bleed wide (16:9 or wider)
**The memory — sketchbook pillar.**
Knowledge Graph (force-directed map of everything you've made) or the Vault listing real sessions. Whichever looks richer with your actual data.

---

## SUBPAGE — 7 slots
File: `composure/index.html`
Currently: all seven are **hand-built CSS/SVG recreations** — not one real capture on the page.

### 5. `01-sidebar.png`
Left rail, full height. All rooms visible + Scribe status. Proves the scope in one glance.

### 6. `02-sketch.png`
Sketch room, mid-drawing. Ink strokes on the canvas, playhead visible.

### 7. `03-radio.png`
Radio room, live, with a prompt typed in and the station responding.

### 8. `04-drum-forge.png`
Step sequencer with a kit loaded. Wide — this slot is full-width on the page.

### 9. `05-dungeon-master.png`
A quest card with its criteria visible (the "play a cohesive 16-bar melody in 7/8" type of thing).

### 10. `06-synth-forge.png`
Patch editor + the Chladni-plate visualizer if it's showing.

### 11. `07-composer.png`
Piano roll + the rendered sheet music. Sheet music is the money shot here.

---

## PROPOSED — 3 new slots the copy needs but has nowhere to live

The rewrite is going to lean on **DAW control / MIDI routing**, and right now there is **no image slot anywhere** for it. If you can grab these, I'll add the sections.

### 12. `08-midi-routing.png`
**The DAW control proof.** Two options, either works:
- The virtual MIDI output port visible **inside a DAW** (Ableton / Maschine / FL Studio) as a selectable input, or
- Composure's MIDI settings showing the port + the MIDI clock running.

### 13. `09-tablet-controller.png`
Android app running, connected to the desktop, showing the controller surface. Phone or tablet. This is the "stage on your desk / studio in your bag" claim made real.

### 14. `10-midi-input.png`
**Settings → MIDI Input Device dropdown, open, with your actual device listed.**

⚠️ **This one matters for a claim.** You said *Bluetooth MIDI control*. I grepped the entire Composure codebase — every file type, excluding node_modules — and there are **zero** Bluetooth/BLE references. What genuinely exists: Web MIDI (any input the OS exposes, which **includes BLE-MIDI devices**), a virtual MIDI output port, and MIDI Clock at 24 PPQ with start/stop for DAW transport sync.

So: if you pair a Bluetooth MIDI keyboard and it shows up in that dropdown, the copy can say Bluetooth MIDI and this screenshot is the receipt. If the device you actually use is the MX88 over USB, the copy says hardware MIDI and we don't claim Bluetooth. **Send me this shot and I'll write the true version.** I'm not writing "Bluetooth" into a page until I've seen it on screen.

---

## What I'm doing while you shoot

Rewriting the article. Your read is correct and I can back it with specifics — the existing piece is both **salesy and factually stale**:

- Claims **five channels**. The app has **sixteen**, with five default roles.
- Names the channels Drums/Lead/Melody/Ambience/Bass. The subpage says Drums/Bass/Chords/Melody. Neither is verified — I'll pull the real map.
- **Missing every feature that makes it valuable.** Keyword audit against the live article: MCP = 0. DAW names = 0. Android = 0. Basic Pitch = 0. Drum Forge = 0. Synth Forge = 0. Soundscapes = 0. Dungeon Master = 0. Knowledge Graph = 0. Obsidian = 0. Radio = 0. Virtual MIDI = 0. Substrate = 0. Clock sync = 0. Vault = 0.
- Its four images are illustrations of an idea, not the app.

The subpage is far more accurate — it just has no real images. So: article gets rewritten around the three real pillars, subpage keeps its bones and swaps mockups for your shots.

**The three pillars, in your words:**
1. **Sonic sketchbook** — Scribe, capture without ceremony, Vault, Knowledge Graph, export to Obsidian
2. **Agentic collaborator** — MCP surface, Substrate, transform-not-regenerate, moods
3. **Control surface** — virtual MIDI out, MIDI clock, DAW transport, tablet as remote controller

No analogies. No "refuses the timeline metaphor." Just what it does and why that's worth having.
