# House News — Image Art Direction & Style Guide

**Status:** CONFIRMED (Aug 26, 2026) — after the v0 → v3 moodboard process.
**Model:** Flux 2 Pro (`black-forest-labs/flux.2-pro`) via OpenRouter.
**One line:** Every image should feel like a page from the same scrapbook, made by one patient artist — either a *studied specimen* or a *witnessed moment*. Never a glossy AI render.

This file is the single source of truth for House News image generation.
Build every prompt from the skeletons in §7. If an image doesn't pass §2 and §3, it's wrong.

---

## 0. The Unifying Frame

**One artist's scrapbook.** All House News images — heroes, inline figures, index cards — are pages from the same book. Same hand, same palette, same restraint.

If two images from different issues don't look like they could sit on the same shelf, one of them is wrong. Consistency across the board is the point, not per-image cleverness.

---

## 1. The Two Lanes

Every image is either **Lane A** or **Lane B**.
(Lane C — infrared / print-grain — is **PARKED**, not yet owned. Do not use it.)

### Lane A — Specimen Plate (illustration)
*Register: "We studied this object." Contemplative, archival, scientific.*

- 19th-century naturalist scientific plate
- Sepia ink with faint graphite construction lines still visible underneath
- Heavyweight cream cold-press watercolor paper, visible tooth, deckled warmth
- Precise observational linework; cross-hatching for shadow
- Small handwritten-style latin labels that feel **etched into the page**, not decorative
- A single muted ochre wash (or one copper accent) — restraint, not color
- Calm, centered composition like a botanical plate
- **Only ink, graphite, and paper.** No tape, clips, swatches, margin notes, or collage.
- "Feels like one patient artist's hand studied the machine."

### Lane B — Documentary Photojournalism (photoreal)
*Register: "We witnessed this in the wild." Newsy, candid, real-world.*

- 35mm Kodak Portra 400 look
- **Full camera spec in every prompt** — film stock + lens + aperture + shutter (e.g. `35mm f/2.8 prime, 1/125s`). Default is the walked-past journalist's kit; vary per scene (§7 lens slot)
- A **real place**, real camera distance (across the street, eye level, wide framing)
- Available light only — overcast, window, dawn, dusk, sodium, fluorescent
- Candid, unposed — a photojournalist who happened to walk past
- Muted earth tones, visible film grain, natural depth of field
- Honest, not staged — "a real press photograph from a news wire service"
- **Scale anchors mandatory** (see §3)

---

## 2. Universal Rules (both lanes)

**DO**
- Muted palette: deep olive · near-black · paper cream / bone white · warm amber light · muted earth tones
- Visible texture: film grain (B), paper tooth (A)
- Wear and patina: scuffed, dusted, aged, used, lived-in
- Negative space; magazine-feature composition
- Restrained, serious, editorial

**DON'T**
- No neon, no electric blue, no rainbow
- No glossy AI look, no studio backdrop, no studio staging
- No rim lighting, no hero lighting, no cinematic mood
- No glow effects, no gradient lighting
- No cute characters, no product-photography polish
- Nothing cartoonishly large or out of place

---

## 3. The Scale Rule (the v3 lesson — non-negotiable)

**Nothing should look cartoonishly large or out of place.**

- Pin real-world scale in the prompt: "roughly the size of a human hand," "hand-sized, normal scale."
- Put **in-frame scale anchors** next to the subject: a coffee mug, a pencil, a human hand, a workbench, a room the subject is dwarfed by.
- No hero cropping that inflates the subject.
- The subject is *one small thing in a real place*, not a centered hero object.

This is what fixed the v2 gripper. If a subject reads as a "cartoon hero," the prompt is missing a scale anchor.

---

## 4. Choosing a Lane (the nuance)

The choice is **editorial register, not subject type.** The same story can go either way.

- **Lane B (default)** — the story is a *happening*: an event, a place, a moment, people in the world. Most hard news. → the **witness** frame.
- **Lane A** — the story's subject is a *thing / mechanism / concept* you want to present as a studied object; you want the contemplative, "pinned under glass" register. Explainers, features, the object itself is the news. → the **specimen** frame.
- **When unsure:** if there's a *scene* in the story, use B. If the story is *about the object itself*, use A.

Both lanes were tested on the same subject (the Open Claw gripper) on purpose — to prove the register, not the subject, is what you're choosing.

---

## 5. Palette & Texture Spec

- **Colors:** deep olive green · near-black · paper cream / bone white · warm amber (light source) · muted earth tones
- **Lane A adds:** sepia ink · muted ochre wash · single copper accent
- **FORBIDDEN:** neon · electric blue · rainbow · glossy
- **Texture:** film grain · paper tooth · dust · scratches · wear · patina · (optional) scanline overlay

---

## 6. Technical

- **Model:** `black-forest-labs/flux.2-pro` (OpenRouter `POST /api/v1/images`)
- **Aspect:** heroes 16:9 · inline figures 4:3
- **Response format:** `b64_json`
- **Output:** `assets/images/` (live heroes) · `assets/moodboard-v*/` (test batches)
- **Review:** contact sheets go to `workspace/image generations/` for the user's file viewer.

---

## 7. Prompt Recipe (build from these)

### Lane A skeleton
> "Naturalist specimen illustration in the style of a 19th-century scientific plate: **[SUBJECT]** drawn in sepia ink with faint graphite construction lines still visible underneath, on heavyweight cream cold-press watercolor paper with visible tooth and deckled warmth. Precise observational linework, cross-hatching for shadow, small handwritten-style latin labels near key parts that feel etched into the page rather than decorative. A single muted ochre wash across one detail like a botanical study. Absolutely no tape, no paper clips, no paint swatches, no margin notes, no collage elements — only ink, graphite and paper. Feels like one patient artist's hand studied [SUBJECT]. 16:9"

### Lane B skeleton
> "Documentary photograph shot on 35mm Kodak Portra 400, **[LENS SPEC — default: 35mm f/2.8 prime, 1/125s]**: **[SUBJECT]** in **[REAL PLACE]**, **[CAMERA DISTANCE — across the street / eye level / wide framing]**, **[AVAILABLE LIGHT — overcast / window / dawn / dusk]**. **[SCALE ANCHOR — hand-sized / a mug and pencil beside it / a human hand holding it / dwarfed by the room]**. Candid, unposed, like a photojournalist who happened to walk past. Muted earth tones, visible film grain, natural depth of field. An honest photograph taken by a person, not staged product photography. No studio backdrop, no glossy reflections, no neon, nothing cartoonishly large, everything to true scale. 16:9"

Fill the bracketed slots per article. Keep everything else verbatim.

**Lens spec slot** — honest photojournalist's kit, never a hero lens:
- `35mm f/2.8 prime, 1/125s` — **default.** Walked past, eye level, subject in context.
- `28mm f/4 prime, 1/125s` — wide environmental, dwarfed-by-the-room (stadium, factory floor, big press).
- `50mm f/2 prime, 1/60s` — tighter, quieter, low light (dusk, interior, sodium).
Aperture stays f/2–f/5.6 — enough falloff to look optical, never creamy portrait bokeh. Shutter honest to the light: 1/60 dusk/dawn, 1/125 overcast, 1/250 bright daylight.

---

## 8. Deprecated (do not resurrect)

- **"SIGNA" style** — neon, cinematic, glowing, futuristic (old manifest entries). Rejected.
- **v1 "ceramic figurine" / cute-object approach.** Rejected — "stupid and AI af."
- **Lane C** — infrared / print-grain. Parked, not owned.
- **Legacy "archival darkroom print / Monocle / scanline / olive-cream-near-black" heroes** — an earlier drift of Lane B. Close, but the **confirmed** Lane B is the **Portra 400 documentary** look. When we do the site-wide refresh, re-grade the legacy heroes toward the §7 Lane B skeleton. (Not now — site refresh is deferred.)

---

## 9. Process

- Small batches (4 images): **discuss → confirm → experiment.** No mass replacement.
- Save contact sheets to `workspace/image generations/` for review.
- When an image lands, lock it into the `gen_images.py` manifest as the confirmed hero.
- One open decision at a time. Don't re-roll a locked lane.
