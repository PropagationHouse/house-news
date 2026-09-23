// Propagation House — merch checkout.
// Creates a Stripe Checkout Session on the fly (payment + shipping address),
// then hands the address to the Printful proxy to create the order.
//
// POST /api/checkout
// Body: { productId, size, quantity? }
// Returns: { url } — the Stripe Checkout Session URL to redirect the buyer to.
//
// The Stripe secret key lives only in this serverless function (env var).
// No manual Payment Links needed — sessions are minted per purchase.

const STRIPE = 'https://api.stripe.com/v1';

// Allowlist: only these three products ever get a checkout.
const ALLOWED_PRODUCTS = new Set([146, 1592, 809]); // hoodie, tee, beanie

// Server-side sold-out guard. The client hides the button, but the server must
// refuse too — otherwise a direct POST to /api/checkout mints a live session
// for a product that loses money. The tee costs $41.96 to fulfill vs $30 price
// = -$11.96/sale, so it is sold out. Keep this in sync with shop-config.js.
const SOLD_OUT_PRODUCTS = new Set([1592]); // Daily Edition Tee (money-loser)

// Price IDs keyed by product. Each product gets its own one-time price.
// (Create these in Stripe > Products. One price per product, not per size.)
const PRICE_MAP = {
  146: process.env.STRIPE_PRICE_HOODIE, // Studio Hoodie
  1592: process.env.STRIPE_PRICE_TEE,   // Daily Edition Tee
  809: process.env.STRIPE_PRICE_BEANIE, // Fisherman Beanie
};

// Map shop size labels to Printful variant ids (mirrors printful-proxy.js).
// NOTE: checkout only passes product_id + size in metadata. The actual Printful
// sync_variant_id is resolved in finalize-order.js from the store's real products.
const VARIANT_MAP = {
  146: { M: 4280269967, L: 4280269969, XL: 4280269974, XXL: 4280269977 },
  1592: { S: 4280294054, M: 4280294055, L: 4280294056, XL: 4280294057, XXL: 4280294058 },
  809: { 'One Size': 4280465855, OS: 4280465855 },
};

module.exports = async (req, res) => {
  const send = (code, msg) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(typeof msg === 'string' ? JSON.stringify({ error: msg }) : JSON.stringify(msg));
  };

  if (req.method !== 'POST') return send(405, 'Method not allowed.');

  // Vercel's Node runtime auto-parses application/json bodies into an object,
  // so req.body may already be an object. Only parse when it's a raw string.
  let body = req.body;
  if (typeof body === 'string') {
    try { body = JSON.parse(body); }
    catch (e) { return send(400, 'Invalid JSON body.'); }
  }
  if (!body || typeof body !== 'object') body = {};

  const productId = parseInt(body.productId, 10);
  const size = body.size;
  if (!ALLOWED_PRODUCTS.has(productId)) return send(403, 'That product is not in the shop.');

  const priceId = PRICE_MAP[productId];
  if (!priceId) return send(500, 'No Stripe price configured for this product.');

  if (SOLD_OUT_PRODUCTS.has(productId)) {
    return send(409, 'That item is sold out — no checkout was created.');
  }

  const map = VARIANT_MAP[productId];
  const variantId = map ? map[size] : null;
  if (!variantId) return send(400, 'Unknown size for that product.');

  const apiKey = process.env.STRIPE_SECRET_KEY;
  if (!apiKey) return send(500, 'Stripe key not configured on server.');

  // Mint a Checkout Session. Stripe collects payment + shipping address.
  // After payment we redirect back to /shop/thanks, which calls the Printful
  // proxy with the address Stripe collected.
  const params = new URLSearchParams({
    mode: 'payment',
    'line_items[0][price]': priceId,
    'line_items[0][quantity]': '1',
    'success_url': (process.env.SHOP_SUCCESS_URL || 'https://propagation.house/shop/thanks') + '?session_id={CHECKOUT_SESSION_ID}',
    'cancel_url': process.env.SHOP_CANCEL_URL || 'https://propagation.house/shop',
    // Always create a Stripe Customer so every buyer has an account to sign in to.
    'customer_creation': 'always',
    'metadata[product_id]': String(productId),
    'metadata[size]': size,
    'shipping_address_collection[allowed_countries][0]': 'US',
    'shipping_address_collection[allowed_countries][1]': 'CA',
  });

  try {
    const r = await fetch(STRIPE + '/checkout/sessions', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: params.toString(),
    });
    const data = await r.json();
    if (!r.ok) {
      return send(502, 'Stripe rejected the session: ' + (data.error && data.error.message ? data.error.message : JSON.stringify(data)));
    }
    return send(200, { url: data.url, sessionId: data.id });
  } catch (e) {
    return send(500, 'Checkout request failed: ' + (e && e.message ? e.message : 'unknown'));
  }
};
