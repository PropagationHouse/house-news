// GET /api/account/me — the signed-in holder's locker.
const auth = require('../../lib/auth');
const stripe = require('../../lib/stripe');
const ent = require('../../lib/entitlements');

module.exports = async (req, res) => {
  const send = (code, payload) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.end(JSON.stringify(payload));
  };

  const s = auth.session(req);
  if (!s) return send(401, { authenticated: false });

  try {
    let customer = null;
    if (s.customer) {
      const r = await stripe.call('GET', '/customers/' + encodeURIComponent(s.customer));
      if (r.ok) customer = r.data;
    }
    const customerId = (customer && customer.id) || s.customer || null;
    const rows = customerId ? await ent.ledgerFor(customerId, s.email) : [];
    const tier = ent.bestTier(rows);
    const md = (customer && customer.metadata) || {};

    return send(200, {
      authenticated: true,
      email: s.email,
      name: (customer && customer.name) || null,
      customer_id: customerId,
      has_billing_portal: !!(customer && customer.id),
      tier: tier,
      can_download: !!tier,
      prefs: {
        alerts: md.optin_alerts === 'true',
        news: md.optin_news === 'true',
      },
      entitlements: rows,
    });
  } catch (e) {
    return send(500, { authenticated: true, error: 'Could not load account: ' + (e && e.message ? e.message : 'unknown') });
  }
};
