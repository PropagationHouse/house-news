// Create 3 Stripe products + prices for merch (hoodie/tee/beanie).
// Run with the live Stripe key. Prints the price IDs to wire as env vars.
const STRIPE = 'https://api.stripe.com/v1';
const key = process.env.STRIPE_SECRET_KEY;
if (!key) { console.error('No STRIPE_SECRET_KEY set'); process.exit(1); }

const items = [
  { name: 'Studio Hoodie', amount: 5500 },
  { name: 'Daily Edition Tee', amount: 3000 },
  { name: 'Fisherman Beanie', amount: 2800 },
];

// URLSearchParams does NOT recurse nested objects (metadata -> "[object Object]").
// Build the form body manually so metadata[source] encodes correctly.
function form(obj) {
  const parts = [];
  for (const [k, v] of Object.entries(obj)) {
    if (typeof v === 'object' && v !== null) {
      for (const [k2, v2] of Object.entries(v)) parts.push(encodeURIComponent(k + '[' + k2 + ']') + '=' + encodeURIComponent(v2));
    } else {
      parts.push(encodeURIComponent(k) + '=' + encodeURIComponent(v));
    }
  }
  return parts.join('&');
}

async function post(path, body) {
  const r = await fetch(STRIPE + path, {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key, 'Content-Type': 'application/x-www-form-urlencoded' },
    body: form(body),
  });
  const d = await r.json();
  if (!r.ok) throw new Error(path + ' failed: ' + (d.error && d.error.message ? d.error.message : JSON.stringify(d)));
  return d;
}

(async () => {
  for (const it of items) {
    const prod = await post('/products', {
      name: it.name,
      description: 'Propagation House merch — ' + it.name,
      metadata: { source: 'house-news-shop' },
    });
    const price = await post('/prices', {
      product: prod.id,
      unit_amount: String(it.amount),
      currency: 'usd',
      metadata: { source: 'house-news-shop' },
    });
    console.log(it.name + ' | product=' + prod.id + ' | price=' + price.id);
  }
})().catch(e => { console.error('ERROR: ' + e.message); process.exit(1); });
