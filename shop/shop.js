/* Propagation House — shop renderer.
   Reads window.PH_SHOP (shop-config.js) and renders the index grid + product pages. */
(function () {
  var S = window.PH_SHOP;
  if (!S) return;

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }
  function money(n) { return "$" + n; }
  function find(slug) {
    for (var i = 0; i < S.products.length; i++) if (S.products[i].id === slug) return S.products[i];
    return null;
  }

  /* ---------------- index ---------------- */
  function renderIndex(mount) {
    var grid = el("div", "shop-grid");
    S.products.forEach(function (p) {
      var card = el("a", "shop-card");
      card.href = "/shop/" + p.id;
      var shot = el("div", "shot");
      var img = document.createElement("img");
      img.src = p.images[0].src; img.alt = p.images[0].alt; img.loading = "lazy";
      shot.appendChild(img);
      if (p.soldOut) shot.appendChild(el("span", "badge", "Sold out"));
      var body = el("div", "body");
      body.appendChild(el("h3", null, p.name));
      body.appendChild(el("p", "sub", p.tagline));
      body.appendChild(el("div", "price", money(p.price)));
      body.appendChild(el("div", "sizes-line", "Sizes " + p.sizes.join(" · ")));
      card.appendChild(shot); card.appendChild(body);
      grid.appendChild(card);
    });
    mount.appendChild(grid);
    var note = el("p", "shop-note", S.soldOutNote + ". The set is limited, and restocks are not on a schedule.");
    mount.appendChild(note);
  }

  /* ---------------- product ---------------- */
  function renderProduct(mount, slug) {
    var p = find(slug);
    if (!p) {
      mount.appendChild(el("p", "shop-missing", "That item is not in the shop. Head back to the shop index."));
      return;
    }
    document.title = p.name + " — Propagation House";

    var back = el("a", "back-link", "\u2190 All merch");
    back.href = "/shop";
    mount.appendChild(back);

    var wrap = el("div", "shop-product");

    /* gallery */
    var gal = el("div", "gallery");
    var stage = el("div", "stage");
    var stageImg = document.createElement("img");
    stageImg.src = p.images[0].src; stageImg.alt = p.images[0].alt;
    stage.appendChild(stageImg);
    var thumbs = el("div", "thumbs");
    p.images.forEach(function (im, i) {
      var b = document.createElement("button");
      b.type = "button";
      if (i === 0) b.className = "on";
      b.setAttribute("aria-label", im.alt);
      var t = document.createElement("img");
      t.src = im.src; t.alt = im.alt; t.loading = "lazy";
      b.appendChild(t);
      b.addEventListener("click", function () {
        stageImg.src = im.src; stageImg.alt = im.alt;
        Array.prototype.forEach.call(thumbs.children, function (c) { c.className = ""; });
        b.className = "on";
      });
      thumbs.appendChild(b);
    });
    gal.appendChild(stage); gal.appendChild(thumbs);

    /* buy column */
    var buy = el("div", "buy");
    buy.appendChild(el("h1", null, p.name));
    buy.appendChild(el("p", "tagline", p.tagline));
    buy.appendChild(el("p", "price", money(p.price)));
    buy.appendChild(el("p", "stock", p.soldOut ? S.soldOutNote : "In stock"));

    var blurb = el("p", "blurb");
    blurb.innerHTML = p.blurb;
    buy.appendChild(blurb);

    /* size picker */
    var label = el("div", "opt-label");
    label.appendChild(el("span", null, p.sizes.length > 1 ? "Size" : "Fit"));
    var chosen = el("span", "chosen", p.sizes.length > 1 ? "Select a size" : p.sizes[0]);
    label.appendChild(chosen);
    buy.appendChild(label);

    var row = el("div", "size-row");
    var current = null;

    var btn = el("button", "buy-btn");
    btn.type = "button";

    function refresh() {
      if (p.soldOut) {
        btn.textContent = S.soldOutNote;
        btn.setAttribute("aria-disabled", "true");
        return;
      }
      var link = current ? p.links[current] : null;
      if (link) {
        btn.textContent = "Add to cart \u2014 " + money(p.price);
        btn.removeAttribute("aria-disabled");
      } else {
        btn.textContent = current ? S.fallbackNote : "Select a size";
        btn.setAttribute("aria-disabled", "true");
      }
    }

    p.sizes.forEach(function (s) {
      var b = el("button", null, s);
      b.type = "button";
      if (p.outOfStock.indexOf(s) !== -1) {
        b.disabled = true;
        b.title = "Sold out in " + s;
      }
      b.addEventListener("click", function () { pick(s, b); });
      row.appendChild(b);
    });
    buy.appendChild(row);

    function pick(s, b) {
      current = s;
      chosen.textContent = s;
      Array.prototype.forEach.call(row.children, function (c) { c.classList.remove("on"); });
      if (b) b.classList.add("on");
      refresh();
    }

    /* single-size items (a beanie) have nothing to choose — select it up front */
    if (p.sizes.length === 1) pick(p.sizes[0], row.firstElementChild);

    btn.addEventListener("click", function () {
      if (btn.getAttribute("aria-disabled") === "true") return;
      var link = p.links[current];
      if (link) window.location.href = link;
    });
    buy.appendChild(btn);
    refresh();

    var under = el("p", "under");
    under.textContent = p.soldOut
      ? "Nothing to buy yet \u2014 this item is between runs."
      : "Checkout is handled by the payment link \u2014 no account needed.";
    buy.appendChild(under);

    /* specs */
    var specs = el("div", "specs");
    specs.appendChild(el("h4", null, "Details"));
    var ul = document.createElement("ul");
    p.details.forEach(function (d) { ul.appendChild(el("li", null, d)); });
    specs.appendChild(ul);
    buy.appendChild(specs);

    wrap.appendChild(gal); wrap.appendChild(buy);
    mount.appendChild(wrap);
  }

  document.addEventListener("DOMContentLoaded", function () {
    var mount = document.getElementById("shop-mount");
    if (!mount) return;
    var mode = mount.getAttribute("data-shop");
    if (mode === "index") renderIndex(mount);
    else {
      var slug = new URLSearchParams(window.location.search).get("p") || mount.getAttribute("data-slug");
      renderProduct(mount, slug);
    }
  });
})();
