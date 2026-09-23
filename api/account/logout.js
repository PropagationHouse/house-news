// GET /api/account/logout — clear the session cookie.
const auth = require('../../lib/auth');

module.exports = async (req, res) => {
  auth.clearCookie(res);
  res.statusCode = 302;
  res.setHeader('Location', '/');
  res.end();
};
