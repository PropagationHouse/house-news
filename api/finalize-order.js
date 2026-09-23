// Propagation House — finalize a merch order after Stripe payment.
// GET /api/finalize-order?session_id=cs_...
// Verifies the checkout session is paid, pulls the shipping address Stripe
// collected, and creates the Printful order (confirmed, since payment is done).
//
// Returns { ok, message, orderId, trackingUrl }.

const PRINTFUL_API = 'https://api.printful.com';

const ALLOWED_PRODUCTS = new Set([146, 1592, 809]);
// Products ordered by the store's SYNC variant id so the attached design ships.
// These are the store's real products (wix store) that carry the designs —
// ordering by catalog variant_id would print a blank garment.
const SYNC_VARIANT_MAP = {
  // Studio Hoodie -> store "PHSDS Daily Edition" (Gildan 18500, Black)
  146: { M: 4280269967, L: 4280269969, XL: 4280269974, XXL: 4280269977 },
  // Daily Edition Tee -> store "Sigil Bone Dust Tee (Embroidered)" (Faded Bone, live)
  // NOTE: the old "Daily Edition Tee" product (383918316) is DISCONTINUED in the store.
  // The live tee is the embroidered Sigil Bone Dust Tee — Faded Bone is the lightest.
  1592: { S: 4280294054, M: 4280294055, L: 4280294056, XL: 4280294057, XXL: 4280294058 },
};

// Products ordered by CATALOG variant id (unprinted — no attached design in the store).
// The fisherman beanie (AS Colour 1120, Black) is NOT a store sync product — the store
// only carries waffle-knit beanies. It's a catalog-only garment, so we order by
// variant_id (20487) and no design is attached (correct for an unprinted hat).
const CATALOG_VARIANT_MAP = {
  809: { 'One Size': 20487, OS: 20487 },
};

// Expected amount in cents per product. The session must have been paid at the
// product's real price — guards against a tampered session or a drifted price.
const EXPECTED_CENTS = { 146: 5500, 809: 2800, 1592: 3000 };

module.exports = async (req, res) => {
  const send = (code, obj) => {
    res.statusCode = code;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.end(JSON.stringify(obj));
  };

  const q = (req && req.query) || {};
  const sid = q.session_id || '';
  if (!/^cs_(live|test)_[A-Za-z0-9]{10,}$/.test(sid)) {
    return send(400, { ok: false, error: 'Missing or invalid session_id.' });
  }

  const stripeKey = process.env.STRIPE_SECRET_KEY;
  const printfulKey = process.env.PRINTFUL_API_KEY;
  if (!stripeKey || !printfulKey) return send(500, { ok: false, error: 'Payment or fulfillment service not configured.' });

  try {
    // 1. Verify the Stripe session is paid and pull the address.
    const sr = await fetch(
      'https://api.stripe.com/v1/checkout/sessions/' + encodeURIComponent(sid) +
      '?expand[]=line_items.data.price',
      { headers: { Authorization: 'Bearer ' + stripeKey } }
    );
    if (!sr.ok) return send(404, { ok: false, error: 'Checkout session not found.' });
    const s = await sr.json();
    if (s.payment_status !== 'paid') return send(402, { ok: false, error: 'Payment not complete.' });

    // 1b. Amount sanity check — the session must have been paid at the real price.
    const paid = typeof s.amount_total === 'number' ? s.amount_total : null;
    const expected = EXPECTED_CENTS[parseInt(s.metadata && s.metadata.product_id, 10)];
    if (expected && paid !== null && paid < expected) {
      return send(402, { ok: false, error: 'Payment amount does not match the product price.' });
    }

    // 1c. Idempotency — Stripe metadata is the record of an order already placed.
    // thanks.js runs on every page load, so without this a refresh double-orders.
    if (s.metadata && s.metadata.ph_order_id) {
      return send(200, { ok: true, message: 'Order already placed — nothing was charged twice.',
                         orderId: s.metadata.ph_order_id });
    }

    const addr = s.shipping_details && s.shipping_details.address;
    const name = (s.shipping_details && s.shipping_details.name) || 'Propagation House Customer';
    if (!addr || !addr.line1) return send(400, { ok: false, error: 'No shipping address on this session.' });

    // 2. Pull product + size from the session metadata (set at checkout).
    const productId = parseInt(s.metadata && s.metadata.product_id, 10);
    const size = s.metadata && s.metadata.size;
    if (!ALLOWED_PRODUCTS.has(productId)) return send(403, { ok: false, error: 'Unknown product in session.' });
    // Order by sync variant id (attached design) for store products, or by
    // catalog variant id for unprinted catalog-only garments (the beanie).
    const syncVariantId = (SYNC_VARIANT_MAP[productId] || {})[size] ||
                          (CATALOG_VARIANT_MAP[productId] || {})[size];
    if (!syncVariantId) return send(400, { ok: false, error: 'That size is not available for this product yet.' });

    // 3. Create the Printful order (confirmed — payment already done).
    const orderBody = {
      external_id: 'house-news-' + sid.slice(0, 20),
      recipient: {
        name: name,
        address1: addr.line1,
        address2: addr.line2 || '',
        city: addr.city || '',
        state_code: addr.state || '',
        zip: addr.postal_code || '',
        country_code: (addr.country || 'US').toUpperCase(),
        phone: '',
      },
      items: [{
        sync_variant_id: syncVariantId,
        quantity: 1,
        name: 'Propagation House merch',
      }],
      // Payment is already confirmed by Stripe, so the order ships.
      status: 'confirmed',
    };

    const pr = await fetch(PRINTFUL_API + '/orders', {
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + printfulKey,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(orderBody),
    });
    const pd = await pr.json();
    if (!pr.ok) {
      return send(502, { ok: false, error: 'Fulfillment failed: ' + (pd.error && pd.error.message ? pd.error.message : JSON.stringify(pd)) });
    }

    const order = pd.result || pd;
    const tracking = order._links && order._links.self ? order._links.self : null;

    // Record the order id on the Stripe session so a page refresh cannot
    // create a second Printful order. Best-effort: the order is already placed.
    try {
      const meta = new URLSearchParams();
      meta.append('metadata[ph_order_id]', String(order.id || ''));
      await fetch('https://api.stripe.com/v1/checkout/sessions/' + encodeURIComponent(sid),
                  { method: 'POST',
                    headers: { Authorization: 'Bearer ' + stripeKey,
                               'Content-Type': 'application/x-www-form-urlencoded' },
                    body: meta.toString() });
    } catch (e) { /* non-fatal */ }

    return send(200, {
      ok: true,
      message: 'Your order is confirmed and heading to print.',
      orderId: order.id,
      trackingUrl: tracking,
    });
  } catch (e) {
    return send(500, { ok: false, error: 'Finalize error: ' + (e && e.message ? e.message : 'unknown') });
  }
};
