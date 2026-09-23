// Propagation House — account auth primitives.
// Deliberately stateless: there is no database. Identity is a Stripe customer;
// a session is a signed token. Nothing to provision, nothing to migrate.
const crypto = require('node:crypto');

const SECRET = process.env.AUTH_SECRET || '';
const COOKIE = 'ph_session';

function b64url(buf) {
  return Buffer.from(buf).toString('base64')
    .replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
function unb64url(s) {
  return Buffer.from(String(s).replace(/-/g, '+').replace(/_/g, '/'), 'base64');
}

function sign(payload, ttlMs) {
  const body = Object.assign({}, payload, { exp: Date.now() + ttlMs });
  const data = b64url(JSON.stringify(body));
  const sig = b64url(crypto.createHmac('sha256', SECRET).update(data).digest());
  return data + '.' + sig;
}

function verify(token) {
  if (!SECRET || typeof token !== 'string') return null;
  const i = token.lastIndexOf('.');
  if (i < 1) return null;
  const data = token.slice(0, i);
  const sig = token.slice(i + 1);
  const want = b64url(crypto.createHmac('sha256', SECRET).update(data).digest());
  const a = Buffer.from(sig);
  const b = Buffer.from(want);
  if (a.length !== b.length || !crypto.timingSafeEqual(a, b)) return null;
  try {
    const p = JSON.parse(unb64url(data).toString('utf8'));
    if (!p.exp || p.exp < Date.now()) return null;
    return p;
  } catch (e) {
    return null;
  }
}

function cookies(req) {
  const raw = (req.headers && req.headers.cookie) || '';
  const out = {};
  raw.split(';').forEach(function (part) {
    const i = part.indexOf('=');
    if (i > 0) out[part.slice(0, i).trim()] = decodeURIComponent(part.slice(i + 1).trim());
  });
  return out;
}

function session(req) {
  return verify(cookies(req)[COOKIE]);
}

function setCookie(res, token, maxAgeSec) {
  res.setHeader('Set-Cookie', [
    COOKIE + '=' + encodeURIComponent(token),
    'Path=/', 'HttpOnly', 'Secure', 'SameSite=Lax', 'Max-Age=' + maxAgeSec,
  ].join('; '));
}

function clearCookie(res) {
  res.setHeader('Set-Cookie', COOKIE + '=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0');
}

module.exports = { sign: sign, verify: verify, cookies: cookies, session: session,
  setCookie: setCookie, clearCookie: clearCookie, COOKIE: COOKIE };
