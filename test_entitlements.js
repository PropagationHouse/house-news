// Local unit test for the entitlement ledger. Synthetic Stripe records,
// no network, no charges. Proves the mapping that the live gate cannot
// exercise without a real payment.
const ent = require('./lib/entitlements');

let fails = 0;
function check(label, cond, extra) {
  if (!cond) fails++;
  console.log((cond ? 'PASS  ' : 'FAIL  ') + label + (extra ? '  ' + extra : ''));
}

const PWYW = ent.PWYW_PRICE;
const BETA = ent.BETA_PRICE;
const NOW = Math.floor(Date.now() / 1000);

// 1. A one-time PWYW purchase -> exe tier, durable.
let rows = ent.buildLedger([{
  kind: 'payment', session_id: 'cs_1', created: NOW, amount: 500,
  prices: [PWYW], names: ['Substrate (PC)'], status: 'paid',
}]);
check('one-time PWYW yields one row', rows.length === 1, 'rows=' + rows.length);
check('  tier is exe', ent.bestTier(rows) === 'exe', 'tier=' + ent.bestTier(rows));
check('  durable flag set', rows[0] && rows[0].durable === true);

// 2. An active Beta subscription -> zip tier.
rows = ent.buildLedger([{
  kind: 'subscription', subscription_id: 'sub_1', created: NOW, status: 'active',
  prices: [BETA], current_period_end: NOW + 86400, cancel_at_period_end: false,
}]);
check('active Beta yields zip tier', ent.bestTier(rows) === 'zip', 'tier=' + ent.bestTier(rows));

// 3. A canceled / past_due subscription grants nothing.
['canceled', 'past_due', 'unpaid', 'incomplete_expired'].forEach(function (st) {
  const r = ent.buildLedger([{
    kind: 'subscription', subscription_id: 'sub_x', created: NOW, status: st,
    prices: [BETA], current_period_end: NOW - 86400,
  }]);
  check('subscription status "' + st + '" grants nothing', ent.bestTier(r) === null,
    'tier=' + ent.bestTier(r));
});

// 4. Both owned -> zip wins (the broader entitlement).
rows = ent.buildLedger([
  { kind: 'payment', session_id: 'cs_a', created: NOW - 100, amount: 500, prices: [PWYW], status: 'paid' },
  { kind: 'subscription', subscription_id: 'sub_b', created: NOW, status: 'active', prices: [BETA] },
]);
check('PWYW + active Beta -> zip wins', ent.bestTier(rows) === 'zip', 'tier=' + ent.bestTier(rows));

// 5. Canceled Beta but owned PWYW -> falls back to exe (never loses what was bought).
rows = ent.buildLedger([
  { kind: 'payment', session_id: 'cs_a', created: NOW - 100, amount: 500, prices: [PWYW], status: 'paid' },
  { kind: 'subscription', subscription_id: 'sub_b', created: NOW, status: 'canceled', prices: [BETA] },
]);
check('canceled Beta falls back to owned exe', ent.bestTier(rows) === 'exe', 'tier=' + ent.bestTier(rows));

// 6. Unknown prices are ignored (merch must not unlock downloads).
rows = ent.buildLedger([
  { kind: 'payment', session_id: 'cs_merch', created: NOW, amount: 5500, prices: ['price_hoodie_fake'], status: 'paid' },
]);
check('merch purchase unlocks nothing', ent.bestTier(rows) === null, 'tier=' + ent.bestTier(rows));
check('  and produces no rows', rows.length === 0, 'rows=' + rows.length);

// 7. Newest first ordering.
rows = ent.buildLedger([
  { kind: 'payment', session_id: 'cs_old', created: NOW - 5000, amount: 500, prices: [PWYW], status: 'paid' },
  { kind: 'subscription', subscription_id: 'sub_new', created: NOW, status: 'active', prices: [BETA] },
]);
check('ledger sorted newest first', rows[0] && rows[0].created === NOW);

// 8. A subscription that produced several invoices still shows one row per product.
rows = ent.buildLedger([
  { kind: 'subscription', subscription_id: 'sub_same', created: NOW, status: 'active', prices: [BETA] },
  { kind: 'subscription', subscription_id: 'sub_same', created: NOW - 1000, status: 'active', prices: [BETA] },
]);
check('same subscription does not duplicate', rows.length === 1, 'rows=' + rows.length);

// 9. File names are stable (this is what makes "latest release" work).
check('exe maps to stable name', ent.FILES.exe === 'Substrate-Setup.exe', ent.FILES.exe);
check('zip maps to stable name', ent.FILES.zip === 'Substrate-Bundle-Desktop-Android.zip', ent.FILES.zip);

console.log('');
console.log('FAILS=' + fails);
process.exit(fails ? 1 : 0);
