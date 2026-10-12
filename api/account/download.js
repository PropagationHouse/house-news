// GET /api/account/download?file=exe|zip|composure-pc|composure-android
//
// The permanent locker: no session_id needed, no 7-day link to lose. The
// entitlement is read live from Stripe on every request and a fresh presigned
// Blob URL is minted, so a reinstalled machine is never locked out.
//
// The gate is the catalog's file list, not a single "best tier": purchases are
// not nested (Composure PC and Composure Android are separate buys), so what
// someone may download is the union of every product they own.

const blob = require('@vercel/blob');
const auth = require('../../lib/auth');
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
  const want = q.file || '';

  try {
    const rows = await ent.ledgerFor(s.customer, s.email);
    const allowed = ent.filesFor(rows);
    if (!allowed.length) return fail(403, 'No purchase with a download is attached to this account.');

    if (allowed.indexOf(want) === -1) {
      return fail(403, 'That file is not part of your purchases.');
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
