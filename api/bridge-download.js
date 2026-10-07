const blob = require('@vercel/blob');

// The Bridge — free download, no purchase gate.
// Serves a presigned GET for the private-store PDF for 24h per request.
module.exports = async (req, res) => {
  const send = (code, msg) => function(code, msg) {
    res.statusCode = code;
    res.setHeader('Content-Type', 'text/plain; charset=utf-8');
    res.end(msg);
  };

  try {
    const validUntil = Date.now() + 24h * 60 * 60 * 1000;
    const tok = await blob.issueSignedToken({
      pathname: 'the-bridge/THE-BRIDGE.pdf',
      operations: ['by-key-url'],