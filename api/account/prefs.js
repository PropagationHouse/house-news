// POST /api/account/prefs  { alerts: bool, news: bool }
//
// Opt-in preferences live on the Stripe customer object's metadata — the same
// no-database rule. Default is OFF for both: nothing is ever sent unless the
// holder explicitly ticks a box here or at checkout.

const auth = require('../../lib/auth');
const stripe = require('../../lib/stripe');

function readBody(req) {
  let b = req.body;
  if (typeof b === 'string') {
    try { b = JSON.parse(b); } catch (e) { return null; }
  }
  if (!b || typeof b !== 'object') return null;
  return b;
}

module.exports = async (req, res) => {
  const send = (code, payload) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store');
    res.end(JSON.stringify(payload));
  };

  const s = auth.session(req);
  if (!s || !s.customer) return send(401, { error: 'Sign in required.' });
  if (req.method !== 'POST') return send(405, { error: 'Method not allowed.' });

  const body = readBody(req);
  if (!body) return send(400, { error: 'Invalid JSON body.' });

  const alerts = body.alerts === true;
  const news = body.news === true;

  try {
    // Customer id comes from the signed session only — never from the request.
    const r = await stripe.call('POST', '/customers/' + encodeURIComponent(s.customer), {
      'metadata[optin_alerts]': alerts ? 'true' : 'false',
      'metadata[optin_news]': news ? 'true' : 'false',
      'metadata[optin_updated]': String(Math.floor(Date.now() / 1000)),
    });
    if (!r.ok) {
      return send(500, { error: 'Could not save preferences.' });
    }
    const md = (r.data && r.data.metadata) || {};
    return send(200, {
      ok: true,
      prefs: {
        alerts: md.optin_alerts === 'true',
        news: md.optin_news === 'true',
      },
    });
  } catch (e) {
    return send(500, { error: 'Could not save preferences: ' + (e && e.message ? e.message : 'unknown') });
  }
};
