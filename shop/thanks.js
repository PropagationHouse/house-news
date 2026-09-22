/* Propagation House — shop thanks page.
   Called by Stripe after a successful payment (success_url).
   Reads the checkout session id from the URL, pulls the shipping address
   Stripe collected, and hands it to the Printful proxy to create the order. */
(function () {
  var sid = new URLSearchParams(window.location.search).get("session_id");
  var statusEl = document.getElementById("order-status");
  var linkEl = document.getElementById("order-link");

  function set(msg, ok) {
    if (statusEl) statusEl.textContent = msg;
    if (linkEl) linkEl.style.display = ok ? "" : "none";
  }

  if (!sid) {
    set("No checkout session found. If you just paid, check your email for the order confirmation.", false);
    return;
  }

  // Ask the server to finalize the order: verify the session, pull the address,
  // and create the Printful order.
  fetch("/api/finalize-order?session_id=" + encodeURIComponent(sid))
    .then(function (r) { return r.json(); })
    .then(function (d) {
      if (d.ok) {
        set("Order confirmed \u2014 " + (d.message || "thanks for the support."), true);
        if (linkEl) linkEl.href = d.trackingUrl || "/shop";
      } else {
        set(d.error || "We could not finalize the order. Contact us with your session id: " + sid, false);
      }
    })
    .catch(function () {
      set("We could not reach the order service. Contact us with your session id: " + sid, false);
    });
})();
