const { put } = require('@vercel/blob');
const fs = require('fs');
const path = require('path');

const PDF = 'C:\\Users\\Bl0ck\\Desktop\\Drop Folder\\THE BRIDGE.pdf';
const TOKEN = fs.readFileSync(path.join(__dirname, 'blob-token.txt'), 'utf8').trim();

(async () => {
  const size = fs.statSync(PDF).size;
  console.log('uploading', (size / 1e6).toFixed(1), 'MB ...');
  const t0 = Date.now();
  const res = await put('the-bridge/THE-BRIDGE.pdf', fs.createReadStream(PDF), {
    access: 'private',
    addRandomSuffix: false,
    allowOverwrite: true,
    contentType: 'application/pdf',
    token: TOKEN,
  });
  console.log('done in', ((Date.now() - t0) / 1000).toFixed(0), 's');
  console.log('URL:', res.url);
  fs.writeFileSync(path.join(__dirname, 'bridge-blob-url.txt'), res.url + '\n');
  console.log('WROTE URL FILE');
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });