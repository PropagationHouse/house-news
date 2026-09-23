// Propagation House — magic-link sign-in.
//
// POST /api/auth/login  { email }        -> always 200 (no account enumeration)
// GET  /api/auth/login?token=...          -> sets session cookie, redirects
//
// Sessions are signed cookies (lib/auth.js). Nothing is stored server-side, so
// "logged in" survives deploys and there is no session table to keep alive.

const auth = require('../../lib/auth');
const stripe = require('../../lib/stripe');
const mail = require('../../lib/mail');

const LINK_TTL_MS = 15 * 60 * 1000;
const SESSION_TTL_MS = 30 * 24 * 60 * 60 * 1000; // 30 days
const SESSION_TTL_SEC = 30 * 24 * 60 * 60;

function readBody(req) {
  let b = req.body;
  if (typeof b === 'string') {
    try { b = JSON.parse(b); } catch (e) { return {}; }
  }
  if (!b || typeof b !== 'object') b = {};
  return b;
}

function send(res, code, payload) {
  res.statusCode = code;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(payload));
}

function baseUrl(req) {
  const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0];
  const host = req.headers['x-forwarded-host'] || req.headers.host || 'propagation.house';
  return proto + '://' + host;
}

function normalEmail(v) {
  const e = String(v || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e) || e.length > 200) return null;
  return e;
}

module.exports = async (req, res) => {
  if (!process.env.AUTH_SECRET) return send(res, 500, { error: 'Auth not configured on server.' });

  // ---- Completing the link ------------------------------------------------
  if (req.method === 'GET') {
    const q = req.query || {};
    const token = q.token || '';
    const next = /^\/[A-Za-z0-9_\-./?=&%]*$/.test(q.next || '') ? q.next : '/account';
    if (token) {
      const p = auth.verify(token);
      if (!p || p.typ !== 'magic' || !p.email) {
        res.statusCode = 302;
        res.setHeader('Location', '/account/login?error=expired');
        res.end();
        return;
      }
      auth.setCookie(res, auth.sign({
        email: p.email,
        customer: p.customer || null,
      }, SESSION_TTL_MS), SESSION_TTL_SEC);
      res.statusCode = 302;
      res.setHeader('Location', next);
      res.end();
      return;
    }
    return send(res, 400, { error: 'Missing token.' });
  }

  if (req.method !== 'POST') return send(res, 405, { error: 'Method not allowed.' });

  const body = readBody(req);
  const email = normalEmail(body.email);
  if (!email) return send(res, 400, { error: 'Enter a valid email address.' });

  try {
    // Look up the Stripe customer. If they have never bought anything there is
    // no account to sign in to — but we say the same thing either way.
    const customer = await stripe.findCustomerByEmail(email);
    const base = baseUrl(req);
    let devLink = null;

    if (customer) {
      const token = auth.sign({ typ: 'magic', email: email, customer: customer.id }, LINK_TTL_MS);
      const link = base + '/api/auth/login?token=' + encodeURIComponent(token) + '&next=' + encodeURIComponent('/account');
      const msg = mail.magicLinkEmail(link);
      const result = await mail.send(email, 'Your sign-in link — Propagation House', msg.text, msg.html);
      // Surface the link in the response ONLY when no mail provider is
      // configured at all AND dev links are explicitly enabled (local work).
      // It must NEVER be returned when a provider exists and the send failed:
      // that would hand a working sign-in link to anyone who knows the address.
      // Triggers for a failed send are mundane — unverified domain, rate limit,
      // provider outage — so this is not a theoretical path.
      if (!result.configured && process.env.AUTH_DEV_LINKS === '1') devLink = link;
    }

    return send(res, 200, {
      ok: true,
      message: 'If that email has an account, a sign-in link is on its way.',
      mail_configured: mail.configured(),
      dev_link: devLink,
    });
  } catch (e) {
    return send(res, 500, { error: 'Sign-in failed: ' + (e && e.message ? e.message : 'unknown') });
  }
};
