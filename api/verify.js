const blob = require('@vercel/blob');

// Allowlist: only these two prices ever unlock a download.
const PRICE_MAP = {
  'price_1ThGrz2Qx6iNdTCBPtrQbl0E': 'exe',   // PWYW one-time (Substrate PC)
  'price_1UDBka2Qx6iNdTCBLnN0ciIZ': 'zip',   // $11.99/mo Beta
};
const FILES = {
  exe: 'Substrate-Setup.exe',
  zip: 'Substrate-Bundle-Desktop-Android.zip',
};

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

    const items = (s.line_items && s.line_items.data) || [];
    let tier = null;
    for (const it of items) {
      const pid = it.price && it.price.id;
      if (pid && PRICE_MAP[pid]) { tier = PRICE_MAP[pid]; break; }
    }
    if (!tier) return send(403, 'This session does not include a Substrate purchase.');

    // Landing mode: bounce to the downloads page, which remembers the session.
    if (q.landing === '1') {
      res.statusCode = 302;
      res.setHeader('Location',
        '/substrate/downloads?session_id=' + encodeURIComponent(sid) +
        '&fresh=1&file=' + tier);
      res.end();
      return;
    }

    const validUntil = Date.now() + SEVEN_DAYS - MARGIN;
    const fkey = (q.file && FILES[q.file]) ? q.file : tier;
    const file = FILES[fkey];
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
