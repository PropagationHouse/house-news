// Expire the smoke-test checkout session so it can't be paid.
const STRIPE = 'https://api.stripe.com/v1';
const key = process.env.STRIPE_SECRET_KEY;
const sid = process.argv[2];
if (!key || !sid) { console.error('usage: node expire.js cs_...'); process.exit(1); }
(async () => {
  const r = await fetch(STRIPE + '/checkout/sessions/' + sid + '/expire', {
    method: 'POST',
    headers: { Authorization: 'Bearer ' + key },
  });
  const d = await r.json();
  console.log('status=' + r.status + ' expired=' + (d.expires_at ? 'yes' : 'no') + ' ' + (d.error ? d.error.message : ''));
})().catch(e => { console.error('ERR ' + e.message); process.exit(1); });
