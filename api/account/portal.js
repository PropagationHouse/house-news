// GET /api/account/portal — redirect to the Stripe Billing Portal so account
// holders can cancel, change card, or download invoices themselves.
//
// The customer id always comes from the signed session, never from the request,
// so one holder can never open another's billing page.

const auth = require('../../lib/auth');
const stripe = require('../../lib/stripe');

module.exports = async (req, res) => {
  const s = auth.session(req);
  if (!s || !s.customer) {
    res.statusCode = 302;
    res.setHeader('Location', '/account/login');
    res.end();
    return;
  }

  try {
    const proto = (req.headers['x-forwarded-proto'] || 'https').split(',')[0];
    const host = req.headers['x-forwarded-host'] || req.headers.host || 'propagation.house';
    const r = await stripe.call('POST', '/billing_portal/sessions', {
      customer: s.customer,
      return_url: proto + '://' + host + '/account',
    });
    if (!r.ok) {
      res.statusCode = 302;
      res.setHeader('Location', '/account?portal=unavailable');
      res.end();
      return;
    }
    res.statusCode = 302;
    res.setHeader('Location', r.data.url);
    res.end();
  } catch (e) {
    res.statusCode = 302;
    res.setHeader('Location', '/account?portal=unavailable');
    res.end();
  }
};
