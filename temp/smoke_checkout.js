// Smoke test: mint a real Stripe Checkout Session for the hoodie via the same
// logic as api/checkout.js, using the live key. Prints the URL + session id.
const STRIPE = 'https://api.stripe.com/v1';
const key = process.env.STRIPE_SECRET_KEY;
if (!key) { console.error('No STRIPE_SECRET_KEY'); process.exit(1); }

function form(obj) {
  const parts = [];
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === 'object' && v !== null) {
      for (const [k2, v2] of Object.entries(v)) parts.push(encodeURIComponent(k + '[' + k2 + ']') + '=' + encodeURIComponent(v2));
    } else parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
  }
  return parts.join('&');
}

(async () => {
  const params = {
    mode: 'payment',
    'line_items[0][price]': 'price_1UIb3w2Qx6iNdTCBw0HAzz1O',
    'line_items[0][quantity]': '1',
    'success_url': 'https://propagation.house/shop/thanks?session_id={CHECKOUT_SESSION_ID}',
    'cancel_url': 'https://propagation.house/shop',
    'metadata[product_id]': '146',
    'metadata[size]': 'M',
    'metadata[variant_id]': '5531',
    'shipping_address_collection[allowed_countries][0]': 'US',
    'shipping_address_collection[allowed_countries][1]': 'CA',
  };
  const r = await fetch(STRIPE + '/checkout/sessions', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form(params),
  });
  const d = await r.json();
  if (!r.ok) { console.error('FAIL ' + r.status + ': ' + (d.error && d.error.message)); process.exit(1); }
  console.log('OK status=' + r.status);
  console.log('session=' + d.id);
  console.log('url=' + d.url);
  console.log('price=' + (d.line_items && d.line_items.data && d.line_items.data[0] && d.line_items.data[0].price && d.line_items.data[0].price.id));
})().catch(e => { console.error('ERR ' + e.message); process.exit(1); });
