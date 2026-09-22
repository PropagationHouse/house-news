// Propagation House — Printful order proxy.
// Serverless function that holds the Printful API key server-side and creates an order.
// The key must NEVER live in browser JS — this is the only place it is read.
//
// POST /api/printful-proxy
// Body: {
//   productId,   // Printful product id (e.g. 146)
//   variantId,   // Printful variant id (e.g. 5530 for hoodie S)
//   quantity,    // int, default 1
//   recipient: { name, address1, city, state, zip, country }
// }
// Returns: { orderId, status, ... } from Printful.
//
// Orders are created as DRAFT by default (status: 'draft') so nothing ships until
// payment is confirmed. Pass confirm:true to create a confirmed order.

const PRINTFUL_API = 'https://api.printful.com';

// Only allow the three products we actually sell. A wrong id ships the wrong garment.
const ALLOWED_PRODUCTS = new Set([146, 1592, 809]); // hoodie, tee, beanie

// Map our shop size labels to Printful variant ids, keyed by product.
const VARIANT_MAP = {
  146: { S: 5530, M: 5531, L: 5532, XL: 5533, XXL: 5534 },       // Gildan 18500 hoodie, black
  1592: { S: 50102, M: 50126, L: 50121, XL: 50097, XXL: 50077 }, // Bella+Canvas 3010 tee, white
  809: { 'One Size': 20487, OS: 20487 },                          // AS Colour 1120 beanie, black
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
  const quantity = Math.max(1, parseInt(body.quantity, 10) || 1);
  const recipient = body.recipient || {};

  // Validate product is one we sell.
  if (!ALLOWED_PRODUCTS.has(productId)) return send(403, 'That product is not in the shop.');

  // Resolve variant id from size. Accept an explicit variantId too.
  let variantId = parseInt(body.variantId, 10);
  if (!variantId) {
    const map = VARIANT_MAP[productId];
    variantId = map ? map[size] : null;
  }
  if (!variantId) return send(400, 'Unknown size for that product.');

  // Validate recipient.
  const need = ['name', 'address1', 'city', 'zip', 'country'];
  for (const f of need) {
    if (!recipient[f]) return send(400, 'Missing recipient field: ' + f);
  }

  const apiKey = process.env.PRINTFUL_API_KEY;
  if (!apiKey) return send(500, 'Printful key not configured on server.');

  const orderPayload = {
    external_id: 'ph-shop-' + productId + '-' + size + '-' + Date.now(),
    recipient: {
      name: recipient.name,
      address1: recipient.address1,
      address2: recipient.address2 || '',
      city: recipient.city,
      state_code: recipient.state || '',
      zip: recipient.zip,
      country_code: recipient.country,
      email: recipient.email || '',
      phone: recipient.phone || '',
    },
    items: [{
      variant_id: variantId,
      quantity: quantity,
    }],
    // Draft by default: nothing ships until payment is verified and we confirm.
    ...(body.confirm ? { status: 'confirmed' } : {}),
  };

  try {
    const r = await fetch(PRINTFUL_API + '/orders', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + apiKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderPayload),
    });
    const data = await r.json();
    if (!r.ok) {
      return send(502, 'Printful rejected the order: ' + (data.error && data.error.message ? data.error.message : JSON.stringify(data)));
    }
    const order = data.result;
    return send(200, {
      orderId: order.id,
      status: order.status,
      externalId: order.external_id,
    });
  } catch (e) {
    return send(500, 'Printful request failed: ' + (e && e.message ? e.message : 'unknown'));
  }
};
