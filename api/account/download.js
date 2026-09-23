// GET /api/account/download?file=exe|zip
//
// The permanent locker: no session_id needed, no 7-day link to lose. The
// entitlement is read live from Stripe on every request and a fresh presigned
// Blob URL is minted, so a reinstalled machine is never locked out.
//
// Tier rules mirror api/verify.js exactly:
//   one-time (exe) -> exe only
//   Beta     (zip) -> zip, and exe too (the desktop build ships inside the bundle)

const blob = require('@vercel/blob');
const auth = require('../../lib/auth');
const stripe = require('../../lib/stripe');
const ent = require('../../lib/entitlements');

const SEVEN_DAYS = 7 * 24 * 60 * 60 * 1000;
const MARGIN = 60 * 60 * 1000;

module.exports = async (req, res) => {
  const fail = (code, msg) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end(msg);
  };

  const s = auth.session(req);
  if (!s || !s.customer) return fail(401, 'Sign in to download.');
  if (!process.env.BLOB_READ_WRITE_TOKEN) return fail(500, 'Delivery not configured on server.');

  const q = req.query || {};
  const want = q.file === 'zip' ? 'zip' : 'exe';

  try {
    const rows = await ent.ledgerFor(s.customer, s.email);
    const tier = ent.bestTier(rows);
    if (!tier) return fail(403, 'No Substrate purchase is attached to this account.');

    if (want !== tier && tier !== 'zip') {
      return fail(403, 'That file is not part of this purchase. The desktop + Android bundle ships with the Beta pass.');
    }

    const file = ent.FILES[want];
    if (!file) return fail(400, 'Unknown file.');

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
    fail(500, 'Delivery error: ' + (e && e.message ? e.message : 'unknown'));
  }
};
