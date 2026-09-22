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

// Price IDs keyed by product. Each product gets its own one-time price.
// (Create these in Stripe > Products. One price per product, not per size.)
const PRICE_MAP = {
  146: process.env.STRIPE_PRICE_HOODIE, // Studio Hoodie
  1592: process.env.STRIPE_PRICE_TEE,   // Daily Edition Tee
  809: process.env.STRIPE_PRICE_BEANIE, // Fisherman Beanie
};

// Map shop size labels to Printful variant ids (mirrors printful-proxy.js).
const VARIANT_MAP = {
  146: { S: 5530, M: 5531, L: 5532, XL: 5533, XXL: 5534 },
  1592: { S: 50102, M: 50126, L: 50121, XL: 50097, XXL: 50077 },
  809: { 'One Size': 20487, OS: 20487 },
};

module.exports = async (req, res) => {
  const send = (code, msg) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(typeof msg === 'string' ? JSON.stringify({ error: msg }) : JSON.stringify(msg));
  };

  if (req.method !== 'POST') return send(405, 'Method not allowed.');

  let body;
  try { body = JSON.parse(req.body || '{}'); }
  catch (e) { return send(400, 'Invalid JSON body.'); }

  const productId = parseInt(body.productId, 10);
  const size = body.size;
  if (!ALLOWED_PRODUCTS.has(productId)) return send(403, 'That product is not in the shop.');

  const priceId = PRICE_MAP[productId];
  if (!priceId) return send(500, 'No Stripe price configured for this product.');

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
    'metadata[product_id]': String(productId),
    'metadata[size]': size,
    'metadata[variant_id]': String(variantId),
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
