const blob = require("@vercel/blob");
const fs = require("fs");
const env = fs.readFileSync(process.env.APPDATA + "\\Substrate\\workspace\\temp\\hn_env_pull.txt", "utf8");
const tok = env.match(/BLOB_READ_WRITE_TOKEN="?([^"\n]+)/)[1];
process.env.BLOB_READ_WRITE_TOKEN = tok;

const FILES = {
  exe: "Substrate-Setup.exe",
  zip: "Substrate-Bundle-Desktop-Android.zip",
  "composure-pc": "Composure-Setup.exe",
  "composure-android": "Composure-Android.apk",
};

(async () => {
  for (const want of ["composure-pc", "composure-android", "exe"]) {
    const file = FILES[want];
    const validUntil = Date.now() + 7*24*60*60*1000 - 60*60*1000;
    const t = await blob.issueSignedToken({ pathname: file, operations: ["get"], validUntil, token: tok });
    const out = await blob.presignUrl(t, { operation: "get", pathname: file, access: "private" });
    const r = await fetch(out.presignedUrl, { method: "HEAD" });
    console.log(want.padEnd(18), file.padEnd(38), "HTTP", r.status, "len", r.headers.get("content-length"));
  }
})().catch(e => { console.error("ERR", e.message); process.exit(1); });
