// Set the 3 merch Stripe price IDs as encrypted Vercel env vars on house-news.
const https = require('https');
const token = require('fs').readFileSync('C:/Users/Bl0ck/AppData/Roaming/Substrate/workspace/vercel/token.txt', 'utf8').trim();
const project = 'prj_FPUXBJovqyrFHS9VPZvPljHtwRX4';

const vars = {
  STRIPE_PRICE_HOODIE: 'price_1UIb3w2Qx6iNdTCBw0HAzz1O',
  STRIPE_PRICE_TEE: 'price_1UIb3x2Qx6iNdTCBfl3Y18Mt',
  STRIPE_PRICE_BEANIE: 'price_1UIb3x2Qx6iNdTCB50kw7CHB',
};

function req(method, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const r = https.request({
      host: 'api.vercel.com', path, method,
      headers: {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json',
        ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}),
      },
    }, (res) => {
      let b = '';
      res.on('data', c => b += c);
      res.on('end', () => {
        let j = null; try { j = JSON.parse(b); } catch (e) {}
        resolve({ status: res.statusCode, json: j });
      });
    });
    r.on('error', reject);
    if (data) r.write(data);
    r.end();
  });
}

(async () => {
  for (const [key, value] of Object.entries(vars)) {
    const out = await req('POST', '/v9/projects/' + project + '/env?upsert=true', {
      key, value, type: 'encrypted',
      target: ['production', 'preview', 'development'],
    });
    console.log(key + ' -> ' + out.status + ' ' + (out.json && out.json.key ? out.json.key : JSON.stringify(out.json)));
  }
})().catch(e => { console.error('ERROR: ' + e.message); process.exit(1); });
