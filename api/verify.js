const blob = require('@vercel/blob');
const ent = require('../lib/entitlements');

// No allowlist lives here. The catalog in lib/entitlements.js is the single
// source of truth for what a price unlocks — this route just asks it.
const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;
const MARGIN = 60 * 60 * 1000; // safety margin for API clock skew

module.exports = async (req, res) => {
  const send = (code, msg) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end(msg);
  };

  const q = (req && req.query) || {};
  const sid = q.session_id || '';
  if (!/^cs_(live|test)_[A-Za-z0-9]{10,}$/.test(sid)) {
    return send(400, 'Missing or invalid session_id.');
  }

  try {
    const sr = await fetch(
      'https://api.stripe.com/v1/checkout/sessions/' + encodeURIComponent(sid) +
      '?expand[]=line_items.data.price',
      { headers: { Authorization: 'Bearer ' + process.env.STRIPE_SECRET_KEY } }
    );
    if (!sr.ok) return send(404, 'Checkout session not found.');
    const s = await sr.json();

    if (s.payment_status !== 'paid') {
      return send(402, 'Payment not complete for this session.');
    }

    // Every price in the session the catalog knows about. A session may carry
    // more than one, so collect them all rather than breaking on the first.
    const items = (s.line_items && s.line_items.data) || [];
    const hits = [];
    for (const it of items) {
      const pid = it.price && it.price.id;
      const entry = pid ? ent.catalogFor(pid) : null;
      if (entry) hits.push(entry);
    }
    if (!hits.length) return send(403, 'This session does not include a purchase with a download.');

    // What this session is allowed to fetch.
    const allowed = [];
    hits.forEach(function (h) {
      (h.files || []).forEach(function (f) {
        if (allowed.indexOf(f) === -1) allowed.push(f);
      });
    });
    const landing = hits[0].landing || '/substrate/downloads';

    // Landing mode: bounce to the product's downloads page, which remembers
    // the session. `file` is the first thing they bought (Substrate's page
    // reads it for its upsell); `files` is the full list, so a page can show
    // exactly the cards this purchase unlocked.
    if (q.landing === '1') {
      res.statusCode = 302;
      res.setHeader('Location',
        landing + '?session_id=' + encodeURIComponent(sid) +
        '&fresh=1&file=' + encodeURIComponent(allowed[0]) +
        '&files=' + encodeURIComponent(allowed.join(',')));
      res.end();
      return;
    }

    // Direct download: the requested file must be one this session unlocked.
    const want = q.file || allowed[0];
    if (allowed.indexOf(want) === -1) {
      return send(403, 'That file is not part of this purchase.');
    }
    const file = ent.FILES[want];
    if (!file) return send(400, 'Unknown file.');

    const validUntil = Date.now() + SEVEN_DAYS - MARGIN;
    const tok = await blob.issueSignedToken({
      pathname: file,
      operations: ['get'],
      validUntil: validUntil,
      token: process.env.BLOB_READ_WRITE_TOKEN,
    });
    const out = await blob.presignUrl(tok, {
      operation: 'get',
      pathname: file,
      access: 'private',
    });

    res.statusCode = 302;
    res.setHeader('Location', out.presignedUrl);
    res.end();
  } catch (e) {
    send(500, 'Delivery error: ' + (e && e.message ? e.message : 'unknown'));
  }
};
