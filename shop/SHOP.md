# Merch shop — how to run it

The shop is live at `/shop`. Three product pages render from one config file.
**Nothing here needs a code change to open checkout.**

## Files

| File | Role |
|---|---|
| `shop/shop-config.js` | **The only file you edit.** Products, prices, sizes, images, links. |
| `shop/index.html` | Shop index shell (`/shop`) |
| `shop/item.html` | Product shell — one page serves all three (`/shop/<slug>`) |
| `shop/shop.css` | House skin + shop layout |
| `shop/shop.js` | Renderer — reads the config, builds the DOM |
| `vercel.json` | Rewrites `/shop/<slug>` → `item.html` |

Images live in `assets/images/merch/` (repo root, not the news subfolder).

## Opening checkout — the actual steps

Today every item is `soldOut: true`, so buttons read *"Sold out — check back soon"*.

For each product you want to sell:

1. Create a payment link (Stripe Payment Link, or any provider that gives you a URL).
   Make one link **per size** if sizes differ in price or stock. Same link for all sizes is fine otherwise.
2. In `shop-config.js`, set `soldOut: false` and fill `links`:

```js
soldOut: false,
links: {
  "S":  "https://buy.stripe.com/xxxx",
  "M":  "https://buy.stripe.com/xxxx",
  "L":  "https://buy.stripe.com/xxxx",
  "XL": "https://buy.stripe.com/xxxx",
  "XXL":"https://buy.stripe.com/xxxx"
}
```

3. Sizes with no link render as *"Checkout opens soon"* and stay disabled — partial rollouts are safe.
4. Sizes that are genuinely gone go in `outOfStock: ["M"]` — shown struck through.

That's it. Commit, push, Vercel deploys.

## Status vocabulary (drives the UI)

| Config | Button shows |
|---|---|
| `soldOut: true` | "Sold out — check back soon" (disabled) |
| `soldOut: false`, no link for chosen size | "Checkout opens soon" (disabled) |
| `soldOut: false`, link present | "Add to cart — $55" (active, links out) |

Single-size items (the beanie) auto-select on load — no dead first click.

## Cart note

This is a **link-out** shop: each size's button goes straight to a payment link.
That is the right shape for three SKUs and matches how Substrate's paid tiers work.
If the range grows past ~8 SKUs or you want a real multi-item cart, that's a
different build (Stripe Checkout with line items, or Snipcart) — say so and I'll scope it.

## Adding a product

Append an object to `products[]` in `shop-config.js` with the same keys, drop its
images into `assets/images/merch/`, then add two rewrites to `vercel.json`:

```json
{ "source": "/shop/<slug>",  "destination": "/shop/item.html" },
{ "source": "/shop/<slug>/", "destination": "/shop/item.html" }
```

The index grid picks it up automatically.

## Images

Source renders are 2000×2000 PNGs with real alpha, in `Desktop\Drop Folder\merch`.
Each product has front / left / right angles (the beanie also has a detail shot) —
those are the galleries. Built to ≤1200px wide, alpha-fringed, in `assets/images/merch/`.
