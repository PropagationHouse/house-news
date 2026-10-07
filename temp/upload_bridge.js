const { put } = require('@vercel/blob');
const fs = require('fs');

(async () => {
  const src = 'C:/Users/Bl0ck/Desktop/Drop Folder/THE BRIDGE.pdf';
  const stream = fs.createReadStream(src, { highWaterMark: 8 * 1024 * 1024 });
  const res = await put('The-Bridge-Fundamentals-of-3D-Spatial-Design.pdf', stream, {
    access: 'private',
    addRandomSuffix: false,
    contentType: 'application/pdf',
    multipart: true,
  });
  console.log('UPLOADED', JSON.stringify(res, null, 2));
})().catch(e => { console.error('FAIL:', e.message); process.exit(1); });