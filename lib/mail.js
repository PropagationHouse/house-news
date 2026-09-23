// Propagation House — transactional mail.
// Provider: Resend (HTTP API, no SDK dependency).
//
// The root domain's mail stays on Proton. Sending happens from a `send.`
// subdomain with its own SPF/DKIM, so the live Proton records are never touched.
// Until RESEND_API_KEY exists, send() returns { configured:false } and callers
// fall back to surfacing the link directly — the account system is fully
// testable before the provider is wired.

const FROM = process.env.MAIL_FROM || 'Propagation House <desk@send.propagation.house>';
const REPLY_TO = process.env.MAIL_REPLY_TO || 'desk@propagation.house';

function configured() {
  return !!process.env.RESEND_API_KEY;
}

async function send(to, subject, text, html) {
  if (!configured()) return { configured: false, sent: false };
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: 'Bearer ' + process.env.RESEND_API_KEY,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: FROM,
        to: [to],
        reply_to: REPLY_TO,
        subject: subject,
        text: text,
        html: html || undefined,
      }),
    });
    const data = await r.json().catch(function () { return {}; });
    return { configured: true, sent: r.ok, status: r.status, data: data };
  } catch (e) {
    return { configured: true, sent: false, error: e && e.message ? e.message : 'unknown' };
  }
}

function magicLinkEmail(link) {
  const text =
    'Here is your sign-in link for Propagation House.\n\n' +
    link + '\n\n' +
    'It expires in 15 minutes and can be used once. If you did not request it, ' +
    'you can ignore this message.\n\n' +
    '— Propagation House\n';
  const html =
    '<div style="font-family:Georgia,serif;color:#1a1d12;line-height:1.6;max-width:520px">' +
    '<p>Here is your sign-in link for Propagation House.</p>' +
    '<p><a href="' + link + '" style="color:#4b5320">Sign in to your account</a></p>' +
    '<p style="font-size:13px;color:#6b6f5a">The link expires in 15 minutes and can be used once. ' +
    'If you did not request it, you can ignore this message.</p>' +
    '<p style="font-size:13px;color:#6b6f5a">— Propagation House</p>' +
    '</div>';
  return { text: text, html: html };
}

module.exports = { send: send, configured: configured, magicLinkEmail: magicLinkEmail, FROM: FROM };
