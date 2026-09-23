// Propagation House — shared Stripe REST helpers (no SDK, no extra dependency).
const API = 'https://api.stripe.com/v1';

function key() {
  const k = process.env.STRIPE_SECRET_KEY;
  if (!k) throw new Error('Stripe key not configured on server.');
  return k;
}

// form: plain object; values may be arrays of objects/strings.
// Objects are flattened to Stripe's bracket notation (metadata[a]=b).
function encode(form, prefix, out) {
  out = out || [];
  Object.keys(form).forEach(function (k) {
    const v = form[k];
    if (v === undefined || v === null) return;
    const name = prefix ? prefix + '[' + k + ']' : k;
    if (Array.isArray(v)) {
      v.forEach(function (item, i) {
        const idx = name + '[' + i + ']';
        if (item && typeof item === 'object') encode(item, idx, out);
        else out.push([idx, String(item)]);
      });
    } else if (typeof v === 'object') {
      encode(v, name, out);
    } else {
      out.push([name, String(v)]);
    }
  });
  return out;
}

async function call(method, path, form) {
  const init = {
    method: method,
    headers: { Authorization: 'Bearer ' + key() },
  };
  if (form) {
    init.headers['Content-Type'] = 'application/x-www-form-urlencoded';
    init.body = encode(form).map(function (p) {
      return encodeURIComponent(p[0]) + '=' + encodeURIComponent(p[1]);
    }).join('&');
  }
  const r = await fetch(API + path, init);
  const data = await r.json().catch(function () { return {}; });
  return { ok: r.ok, status: r.status, data: data };
}

function esc(s) {
  // Stripe search syntax: escape single quotes and backslashes.
  return String(s == null ? '' : s).replace(/\\/g, '\\\\').replace(/'/g, "\\'");
}

async function findCustomerByEmail(email) {
  // IMPORTANT: /customers/search is *eventually consistent* — a customer created
  // seconds ago (i.e. someone who just bought) is not indexed yet, so a
  // brand-new buyer would be told "check your email" and get nothing.
  // The list endpoint filtered by email is immediately consistent, so it is the
  // primary lookup; Search is only a fallback for large accounts.
  const lr = await call('GET', '/customers?limit=10&email=' + encodeURIComponent(email));
  if (lr.ok && lr.data && lr.data.data) {
    const exact = lr.data.data.filter(function (c) {
      return String(c.email || '').toLowerCase() === String(email).toLowerCase();
    });
    if (exact.length) {
      // Prefer a customer that actually has a subscription attached.
      exact.sort(function (a, b) { return (b.created || 0) - (a.created || 0); });
      return exact[0];
    }
  }

  const q = "email:'" + esc(email) + "'";
  const r = await call('GET', '/customers/search?query=' + encodeURIComponent(q) + '&limit=1');
  if (r.ok && r.data && r.data.data && r.data.data.length) return r.data.data[0];
  return null;
}

// Pull every payment that could carry a delivery entitlement.
// Account holders are few, so one page of each is plenty.
async function entitlementsFor(customerId, email) {
  const out = [];
  const seen = {};

  const push = function (o) {
    const id = o.session_id || o.payment_intent || o.id;
    if (!id || seen[id]) return;
    seen[id] = 1;
    out.push(o);
  };

  // One-time purchases (PWYW Substrate, merch, anything else).
  const sessions = await call('GET',
    '/checkout/sessions?limit=100&customer=' + encodeURIComponent(customerId) +
    '&expand[]=data.line_items.data.price');
  if (sessions.ok) {
    ((sessions.data.data) || []).forEach(function (s) {
      if (s.payment_status !== 'paid') return;
      const items = (s.line_items && s.line_items.data) || [];
      const prices = items.map(function (it) {
        return it.price ? it.price.id : null;
      }).filter(Boolean);
      const names = items.map(function (it) {
        return (it.description || (it.price && it.price.nickname) || '').trim();
      }).filter(Boolean);
      push({
        kind: 'payment',
        session_id: s.id,
        payment_intent: s.payment_intent,
        created: s.created,
        amount: s.amount_total,
        currency: s.currency,
        prices: prices,
        names: names,
        mode: s.mode,
        email: (s.customer_details && s.customer_details.email) || email || '',
      });
    });
  }

  // Subscriptions (the Beta pass).
  const subs = await call('GET',
    '/subscriptions?limit=100&customer=' + encodeURIComponent(customerId) +
    '&expand[]=data.items.data.price');
  if (subs.ok) {
    ((subs.data.data) || []).forEach(function (sub) {
      const items = (sub.items && sub.items.data) || [];
      const prices = items.map(function (it) { return it.price ? it.price.id : null; }).filter(Boolean);
      const names = items.map(function (it) {
        return (it.price && it.price.nickname) || '';
      }).filter(Boolean);
      push({
        kind: 'subscription',
        subscription_id: sub.id,
        created: sub.created,
        status: sub.status,
        current_period_end: sub.current_period_end,
        cancel_at_period_end: sub.cancel_at_period_end,
        prices: prices,
        names: names,
        email: email || '',
      });
    });
  }

  // Newest first — the locker reads top-down.
  out.sort(function (a, b) { return (b.created || 0) - (a.created || 0); });
  return out;
}

module.exports = {
  call: call,
  encode: encode,
  esc: esc,
  findCustomerByEmail: findCustomerByEmail,
  entitlementsFor: entitlementsFor,
};
