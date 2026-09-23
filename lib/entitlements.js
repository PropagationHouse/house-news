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

const FILES = {
  exe: 'Substrate-Setup.exe',
  zip: 'Substrate-Bundle-Desktop-Android.zip',
};

// What each price grants. `tier` drives the download button; `durable` means
// the entitlement does not expire (one-time buys outlive the session that made them).
const PRICE_CATALOG = {
  [PWYW_PRICE]: {
    product: 'substrate-pc',
    label: 'Substrate for Windows',
    detail: 'One-time purchase — yours to keep',
    tier: 'exe',
    durable: true,
    kind: 'one-time',
  },
  [BETA_PRICE]: {
    product: 'substrate-beta',
    label: 'Substrate Beta Pass',
    detail: 'Every new build the day it lands — PC and Android',
    tier: 'zip',
    durable: false, // while subscribed
    kind: 'subscription',
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
function bestTier(rows) {
  const live = rows.filter(function (r) { return r.active; });
  if (live.some(function (r) { return r.tier === 'zip'; })) return 'zip';
  if (live.some(function (r) { return r.tier === 'exe'; })) return 'exe';
  return null;
}

async function ledgerFor(customerId, email) {
  const records = await stripe.entitlementsFor(customerId, email);
  return buildLedger(records);
}

module.exports = {
  PWYW_PRICE: PWYW_PRICE,
  BETA_PRICE: BETA_PRICE,
  FILES: FILES,
  PRICE_CATALOG: PRICE_CATALOG,
  catalogFor: catalogFor,
  buildLedger: buildLedger,
  bestTier: bestTier,
  ledgerFor: ledgerFor,
};
