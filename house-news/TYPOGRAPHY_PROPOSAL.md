# Studio Typography Proposal — propagation.house (studio front)

**Status:** PROPOSAL ONLY — no site changes made. Every item is your call.
**Source:** overnight probe sessions (Sep 20, ~1:30–6:11 AM), 16 scripts, verified against live computed styles.
**Scope:** studio root `index.html` only. News front + articles excluded (own rhythm, already gated).

---

## 1. What the page already does well (keep, don't touch)

The skeleton is a working newspaper system:

- **Serif display + sans body** — Playfair Display (900 labels, 700 card titles) over the sans body. Correct instinct, correctly weighted.
- **The scale ladder** — 72px hero → 52px section labels → 52px feature h2s → 32px newsletter → 22px cards → 13px deks. Clean hierarchy, no competing sizes at one level.
- **Kicker discipline** — 10–11px, uppercase, tracked, olive accent, same everywhere. The page's connective tissue.
- **One-hand rule** — em-dash rhythm, pull-quotes, drop-caps on journal pages. The "one patient hand" voice is already in the type.

**Palette tokens (for reference):** ink `#1a1d12`, paper `#f6f1e2`, rule `#c8c3ad`, accent `#4b5320`, accent-dark `#3a4018`, muted `#6b6e5a`.

---

## 2. The one real bug: `<em>` has no CSS rule

**Finding:** all 16 `<em>` uses in headlines ("Walmart *Unlimited*", "The Hall That Holds the *World*", "The Brakes Get *Sued*") render via **browser-default italic** — there is no `em` rule anywhere in the studio CSS.

It works today only because Playfair's italic happens to be loaded. Fragile: any font-load failure silently degrades the signature move. And default italic is the weakest version of the gesture.

**Proposal — codify the signature move:**

```css
/* Headline emphasis: the house signature. Deliberate, not default italic. */
.feature h2 em,
.section-head .label em,
.hero h1 em,
.newsletter h2 em {
  font-style: italic;
  font-weight: 900;
  font-size: 1.02em;      /* italic lifts slightly above roman caps */
  letter-spacing: -0.015em;
  color: var(--accent-dark);
  padding-right: 0.06em;  /* italic overhang protection */
  font-synthesis: none;   /* never synthesize italic if font fails */
}
```

Selector list should cover every headline surface that uses `<em>` (16 current uses verified).

**Why:** the em is the page's most distinctive typographic move — it's what makes headlines feel hand-set. Right now it's an accident that works. Codifying makes it *designed*.

**Cost:** one CSS block. **Risk:** near zero. **Reversible:** one delete.

---

## 3. Kicker system: two sizes, three trackings, no tokens

**Finding:** kickers run at two sizes — 11px (hero, section heads, about lede, composure band) and 10px (lead-feature, lead-story, ss-items, mm-cards, un/mm features, prod cards). Tracking runs at three values — `.2em` (doors), `.15em` (features), `.12em` (items).

The size split reads as a coherent two-tier system: 11px = corridor doors, 10px = interior items. But it's undocumented and unenforced — nothing stops the next feature from using 11px where 10px belongs. And `.12em` at 10px is tight for tracked uppercase — the difference between "tracked" and "squeezed."

**Proposal:** make the two tiers explicit tokens, align tracking to the same tiers:

```css
:root {
  --kicker-lg-size: 11px;   --kicker-lg-track: .2em;   /* doors */
  --kicker-sm-size: 10px;   --kicker-sm-track: .15em;  /* items */
}
```

Items move .12em → .15em: ~0.3px per char at 10px — imperceptible per character, but every card kicker breathes the same as its parent door.

**Cost:** tokens + ~6 rule edits. **Risk:** near zero. **Reversible:** trivial.

---

## 4. The real opportunity: feature deks read small

Reading text runs 13px-18px across six sizes. That compression is a *feature* of newspaper style - the whole point is density. Do not flatten it. But there is one spot where it inverts the emphasis:

| Surface | Size | Role |
|---|---|---|
| hero dek | 18px | hero selling text |
| flagship dek | 17px | flagship selling text |
| un/mm feature deks | 15px | corridor selling text (UN hall, Walmart) |
| card deks | 13px | navigational, fine |

The two feature deks are the text a visitor actually reads on this page - the selling text of the corridor - and they sit at 15px under 52px h2s, smaller than the flagship's 17px. Inverted emphasis.

**Proposal:** lift `#un-feature .dek, #mm-feature .dek` 15px -> 16px. One rule.

**Why only this:** 15->16 is a 7% lift - perceptible side-by-side, invisible in isolation. It fixes the inversion without flattening the scale.

**Cost:** one rule. **Risk:** low but real - the features are geometry-gated (center-column budget, shared-divider stack). 15->16px may shift line wraps. **Gate:** re-run the feature-stack geometry check after the change.

---

## 5. The thing I argue against: a second serif

The temptation: a second serif for pull-quotes (EB Garamond is the usual suspect). My argument: **one serif is the identity.** Playfair at 900 for labels, 700 for cards, italic for ems and pull-quotes - the weight range IS the range. A second serif fragments the one-hand rule. The page's authority comes from restraint: one serif, one sans, one accent, one em gesture. Don't.

---

## 6. Summary

| # | Change | Cost | Risk | Rec |
|---|---|---|---|---|
| 1 | Codify `<em>` headline emphasis | one CSS block | near zero | DO |
| 2 | Kicker tokens (11/10px, .2/.15em) | tokens + 6 edits | near zero | DO |
| 3 | Feature deks 15 -> 16px | one rule | low (geometry gate) | DO |
| 4 | Second serif for pull-quotes | font import + rules | medium | DON'T |
| 5 | Flatten the body scale | - | - | DON'T (density is the style) |

**If you approve 1-3:** implementation is one session, CSS-only, gated (brace balance, geometry check, live verify). Nothing touches copy, images, or the news front.