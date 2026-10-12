// Propagation House — entitlement ledger.
//
// There is no database. The ledger is derived: Stripe holds what was bought,
// this maps it to what can be downloaded. Stable Blob object names mean
// "latest release" needs no version bookkeeping.
//
// Adding a future product = one entry in PRICE_CATALOG. Nothing else changes.

const stripe = require('./stripe');

const PWYW_PRICE = 'price_1ThGrz2Qx6iNdTCBPtrQbl0E';  // Substrate (PC), name-your-price
const BETA_PRICE = 'price_1UDBka2Qx6iNdTCBLnN0ciIZ';  // Substrate Beta, $11.99/mo

// Composure — one-time, sold per platform plus a bundle.
const COMPOSURE_ANDROID_PRICE = 'price_1UPfo12Qx6iNdTCBohszINuw';  // $12
const COMPOSURE_PC_PRICE = 'price_1UPfo22Qx6iNdTCB4WtVYGUc';       // $16
const COMPOSURE_BOTH_PRICE = 'price_1UPfo22Qx6iNdTCBxTPIenoh';     // $22.44

const FILES = {
  // Substrate
  exe: 'Substrate-Setup.exe',
  zip: 'Substrate-Bundle-Desktop-Android.zip',
  // Composure
  'composure-pc': 'Composure-Setup.exe',
  'composure-android': 'Composure-Android.apk',
};

// What each price grants.
//   files   — the Blob objects this purchase unlocks. This is the real gate:
//             a price grants exactly the files it lists, nothing more.
//   tier    — legacy single-string label, kept so Substrate's downloads page
//             and the locker keep working unchanged.
//   landing — where a fresh checkout is bounced to remember its session.
//   durable — one-time buys outlive the session that made them.
const PRICE_CATALOG = {
  [PWYW_PRICE]: {
    product: 'substrate-pc',
    label: 'Substrate for Windows',
    detail: 'One-time purchase — yours to keep',
    files: ['exe'],
    tier: 'exe',
    landing: '/substrate/downloads',
    durable: true,
    kind: 'one-time',
  },
  [BETA_PRICE]: {
    product: 'substrate-beta',
    label: 'Substrate Beta Pass',
    detail: 'Every new build the day it lands — PC and Android',
    files: ['exe', 'zip'],
    tier: 'zip',
    landing: '/substrate/downloads',
    durable: false, // while subscribed
    kind: 'subscription',
  },
  [COMPOSURE_ANDROID_PRICE]: {
    product: 'composure-android',
    label: 'Composure for Android',
    detail: 'One-time purchase — yours to keep',
    files: ['composure-android'],
    tier: 'composure-android',
    landing: '/composure/downloads',
    durable: true,
    kind: 'one-time',
  },
  [COMPOSURE_PC_PRICE]: {
    product: 'composure-pc',
    label: 'Composure for Windows',
    detail: 'One-time purchase — yours to keep',
    files: ['composure-pc'],
    tier: 'composure-pc',
    landing: '/composure/downloads',
    durable: true,
    kind: 'one-time',
  },
  [COMPOSURE_BOTH_PRICE]: {
    product: 'composure-both',
    label: 'Composure — PC + Android',
    detail: 'One-time purchase — both builds, yours to keep',
    files: ['composure-pc', 'composure-android'],
    tier: 'composure-both',
    landing: '/composure/downloads',
    durable: true,
    kind: 'one-time',
  },
};

function catalogFor(priceId) {
  return PRICE_CATALOG[priceId] || null;
}

// Turn raw Stripe records into locker rows.
function buildLedger(records) {
  const rows = [];
  records.forEach(function (rec) {
    const hits = (rec.prices || []).map(catalogFor).filter(Boolean);
    if (!hits.length) return;

    // De-duplicate by product so a subscription that produced several
    // invoices still shows one row.
    hits.forEach(function (h) {
      const existing = rows.find(function (r) {
        return r.product === h.product && r.source_id === (rec.subscription_id || rec.session_id);
      });
      if (existing) return;

      const active = rec.kind === 'subscription'
        ? (rec.status === 'active' || rec.status === 'trialing')
        : true;

      rows.push({
        product: h.product,
        label: h.label,
        detail: h.detail,
        tier: h.tier,
        files: h.files || (h.tier ? [h.tier] : []),
        landing: h.landing || null,
        durable: h.durable,
        kind: h.kind,
        active: active,
        source_id: rec.subscription_id || rec.session_id,
        session_id: rec.session_id || null,
        subscription_id: rec.subscription_id || null,
        created: rec.created || 0,
        status: rec.status || 'paid',
        current_period_end: rec.current_period_end || null,
        cancel_at_period_end: !!rec.cancel_at_period_end,
        amount: rec.amount || null,
        currency: rec.currency || 'usd',
        names: rec.names || [],
      });
    });
  });

  rows.sort(function (a, b) { return (b.created || 0) - (a.created || 0); });
  return rows;
}

// Highest download tier the holder is entitled to right now.
// Legacy single-string view: Substrate's downloads page and locker still read
// this. It is a *label*, not a gate — the gate is filesFor() below.
function bestTier(rows) {
  const live = rows.filter(function (r) { return r.active; });
  if (live.some(function (r) { return r.tier === 'zip'; })) return 'zip';
  if (live.some(function (r) { return r.tier === 'exe'; })) return 'exe';
  return null;
}

// Every file the holder may download right now, across every product they own.
// This is the real entitlement: purchases are not nested (Composure PC and
// Composure Android are separate buys), so a single "best tier" cannot express
// what someone owns. Union the file lists of all live rows.
function filesFor(rows) {
  const out = [];
  rows.forEach(function (r) {
    if (!r.active) return;
    (r.files || []).forEach(function (f) {
      if (out.indexOf(f) === -1) out.push(f);
    });
  });
  return out;
}

// Does this holder own a given product? Used to decide which product's
// downloads page should offer what.
function ownsProduct(rows, product) {
  return rows.some(function (r) { return r.active && r.product === product; });
}

async function ledgerFor(customerId, email) {
  const records = await stripe.entitlementsFor(customerId, email);
  return buildLedger(records);
}

module.exports = {
  PWYW_PRICE: PWYW_PRICE,
  BETA_PRICE: BETA_PRICE,
  COMPOSURE_ANDROID_PRICE: COMPOSURE_ANDROID_PRICE,
  COMPOSURE_PC_PRICE: COMPOSURE_PC_PRICE,
  COMPOSURE_BOTH_PRICE: COMPOSURE_BOTH_PRICE,
  FILES: FILES,
  PRICE_CATALOG: PRICE_CATALOG,
  catalogFor: catalogFor,
  buildLedger: buildLedger,
  bestTier: bestTier,
  filesFor: filesFor,
  ownsProduct: ownsProduct,
  ledgerFor: ledgerFor,
};
