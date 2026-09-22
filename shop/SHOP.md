# Merch shop — how to run it

The shop is live at `/shop`. Three product pages render from one config file.
**Checkout is automated** — payment and fulfillment both run through the API routes.

## Files

| File | Role |
|---|---|
| `shop/shop-config.js` | **The only file you normally edit.** Products, prices, sizes, images, `printfulId`, `soldOut`. |
| `shop/index.html` | Shop index shell (`/shop`) |
| `shop/item.html` | Product shell — one page serves all three (`/shop/<slug>`) |
| `shop/thanks.html` | Post-payment page (`/shop/thanks`) |
| `shop/shop.js` | Renderer — reads the config, builds the DOM, mints checkout sessions |
| `shop/thanks.js` | Confirms the order after payment |
| `shop/shop.css` | House skin + shop layout |
| `api/checkout.js` | Mints a Stripe Checkout Session (payment + shipping address) |
| `api/finalize-order.js` | Verifies the paid session, creates the Printful order |
| `api/printful-proxy.js` | Lower-level Printful order creator (draft by default) — kept as a fallback |
| `vercel.json` | Rewrites `/shop/<slug>` → `item.html`, `/shop/thanks` → `thanks.html` |

Images live in `assets/images/merch/` (repo root, not the news subfolder).

## How a purchase flows

1. Buyer picks a size, hits **Buy — $55**.
2. `shop.js` POSTs `{ productId, size }` to `/api/checkout`.
3. `api/checkout.js` mints a Stripe Checkout Session on the fly — line item keyed to
   that product's price id, shipping address collection on, metadata carrying
   `product_id` / `size` / `variant_id`. Returns a URL; the browser redirects.
4. Stripe collects payment **and the shipping address**.
5. Stripe redirects to `/shop/thanks?session_id=…`.
6. `thanks.js` calls `/api/finalize-order?session_id=…`. That route verifies
   `payment_status === 'paid'`, pulls the address Stripe collected, maps the
   metadata to a Printful variant, and creates a **confirmed** Printful order.

No manual Payment Links, no hand-confirming orders.

## Opening / closing checkout

Everything is driven by `soldOut` in `shop-config.js`:

```js
soldOut: false,   // buttons active
soldOut: true,    // buttons read "Sold out — check back soon" (disabled)
```

To pull a single size, add it to `outOfStock: ["M"]` — shown struck through.
A size is never silently purchasable: the button stays disabled until a size is chosen.

## Environment (Vercel, encrypted)

| Var | What it is |
|---|---|
| `STRIPE_SECRET_KEY` | Live Stripe secret key (already wired for Substrate checkout) |
| `STRIPE_PRICE_HOODIE` | `price_1UIb3w2Qx6iNdTCBw0HAzz1O` |
| `STRIPE_PRICE_TEE` | `price_1UIb3x2Qx6iNdTCBfl3Y18Mt` |
| `STRIPE_PRICE_BEANIE` | `price_1UIb3x2Qx6iNdTCB50kw7CHB` |
| `PRINTFUL_API_KEY` | Printful private token (store `13244328`) |
| `SHOP_SUCCESS_URL` | optional override, default `https://propagation.house/shop/thanks` |
| `SHOP_CANCEL_URL` | optional override, default `https://propagation.house/shop` |

The Printful key lives **only** as an encrypted env var — never on disk, never in browser JS.

## Product → Printful mapping

| Shop slug | `printfulId` | Variants (S/M/L/XL/XXL) |
|---|---|---|
| `house-hoodie` | 146 | 5530 / 5531 / 5532 / 5533 / 5534 |
| `daily-edition-tee` | 1592 | 50102 / 50126 / 50121 / 50097 / 50077 |
| `fisherman-beanie` | 809 | One Size = 20487 |

Changing a price means creating a new Stripe price (or updating the existing one)
and, if the id changes, updating the env var. The config file's `price` field is
display only — Stripe is the source of truth for what's charged.

## Adding a product

1. Create a Stripe product + price; set `STRIPE_PRICE_<NAME>` env var.
2. Append an object to `products[]` in `shop-config.js` with the same keys
   (including `printfulId`).
3. Add its variant map to **both** `api/checkout.js` and `api/finalize-order.js`.
4. Drop its images into `assets/images/merch/`, add two rewrites to `vercel.json`.

## Cart scope

One item per checkout session — right shape for three SKUs. If the range grows
past ~8 SKUs or you want a multi-item cart, that's a Stripe Checkout with
multiple line items rebuild.

## Images

Source renders are 2000×2000 PNGs with real alpha, in `Desktop\Drop Folder\merch`.
Each product has front / left / right angles (the beanie also has a detail shot).
Built to ≤1200px wide, alpha-fringed, in `assets/images/merch/`.

## Gotchas

- **Absolute asset paths only.** Relative refs (`shop.css`, `../assets/…`) break on
  `/shop` without a trailing slash — the browser resolves them against `/`.
- The `/shop/<slug>` rewrite **drops the query string** — the slug is read from
  `window.location.pathname`, not `?p=`.
- `URLSearchParams` does not recurse nested objects — Stripe metadata must be built
  manually as `metadata[key]=value`.
- `Acumin-BPro.otf` does not exist (real file: `Acumin-BdPro.otf`).
