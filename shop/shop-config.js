/* Propagation House — shop config
   Single source of truth for the merch shop. Product pages render from this.
   TO OPEN CHECKOUT: set soldOut:false and paste a payment link into links{size}.
   No other code changes needed. */
window.PH_SHOP = {
  currency: "USD",
  soldOutNote: "Sold out — check back soon",
  fallbackNote: "Select a size",
  products: [
    {
      id: "house-hoodie",
      name: "Studio Hoodie",
      printfulId: 146,
      tagline: "Heavyweight fleece, black",
      price: 55,
      soldOut: false,
      sizes: ["S", "M", "L", "XL", "XXL"],
      outOfStock: [],
      links: {},
      print: "Small mark at the chest",
      blurb: "Heavy-blend fleece with the house mark at the chest. Cut for a straight, roomy fit — the kind of hoodie that survives a studio winter.",
      details: [
        "Heavy-blend fleece, black",
        "Unisex straight fit",
        "Small house mark at the chest",
        "Machine wash cold, inside out"
      ],
      images: [
        { src: "/assets/images/merch/hoodie-1.png", alt: "Studio Hoodie, front" },
        { src: "/assets/images/merch/hoodie-2.png", alt: "Studio Hoodie, left side" },
        { src: "/assets/images/merch/hoodie-3.png", alt: "Studio Hoodie, right side" }
      ]
    },
    {
      id: "daily-edition-tee",
      name: "Daily Edition Tee",
      printfulId: 1592,
      tagline: "Oversized heavyweight cotton, white",
      price: 30,
      soldOut: false,
      sizes: ["S", "M", "L", "XL", "XXL"],
      outOfStock: [],
      links: {},
      print: "Chest print, upper left",
      blurb: "Oversized heavyweight cotton in white, printed at the upper left chest. Built for the desk, the shop floor, and everywhere the work gets carried.",
      details: [
        "Oversized heavyweight cotton, white",
        "Chest print, upper left",
        "Drop shoulder, boxy body",
        "Machine wash cold, inside out"
      ],
      images: [
        { src: "/assets/images/merch/tee-1.png", alt: "Daily Edition Tee, front" },
        { src: "/assets/images/merch/tee-2.png", alt: "Daily Edition Tee, left side" },
        { src: "/assets/images/merch/tee-3.png", alt: "Daily Edition Tee, right side" }
      ]
    },
    {
      id: "fisherman-beanie",
      name: "Fisherman Beanie",
      printfulId: 809,
      tagline: "Ribbed knit, black",
      price: 28,
      soldOut: false,
      sizes: ["One Size"],
      outOfStock: [],
      links: {},
      print: "Unprinted",
      blurb: "A short fisherman's roll in ribbed black knit. Sits above the ear, no mark, no fuss — the quiet piece of the set.",
      details: [
        "Ribbed knit, black",
        "Short fisherman roll",
        "One size, unprinted",
        "Hand wash cold, dry flat"
      ],
      images: [
        { src: "/assets/images/merch/beanie-1.png", alt: "Fisherman Beanie, front" },
        { src: "/assets/images/merch/beanie-2.png", alt: "Fisherman Beanie, left side" },
        { src: "/assets/images/merch/beanie-3.png", alt: "Fisherman Beanie, right side" },
        { src: "/assets/images/merch/beanie-4.png", alt: "Fisherman Beanie, detail" }
      ]
    }
  ]
};
