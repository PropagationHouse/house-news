"""Screenshot the rethemed Composure page so it can be eyeballed."""
import sys, os
from playwright.sync_api import sync_playwright

URL = "http://localhost:8099/composure/"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "temp")

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errors = []
    pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    pg.on("requestfailed", lambda r: errors.append("REQFAIL " + r.url))
    pg.goto(URL, wait_until="networkidle")
    pg.wait_for_timeout(1500)

    pg.screenshot(path=os.path.join(OUT, "teal_hero.png"))
    pg.screenshot(path=os.path.join(OUT, "teal_full.png"), full_page=True)

    # section crops
    for sel, name in [("#two", "two"), ("#collaborator", "collab"), ("#sound", "sound"),
                      ("#rooms", "rooms"), ("#rooms", "rooms")]:
        el = pg.query_selector(sel)
        if el:
            el.screenshot(path=os.path.join(OUT, "teal_%s.png" % name))
        else:
            print("  missing section:", sel)

    h = pg.evaluate("document.body.scrollHeight")
    print("body height:", h)
    print("console errors / failed requests:", errors if errors else "none")

    # sanity: no warm leftovers rendered
    probe = pg.evaluate("""() => {
        const s = getComputedStyle(document.body);
        return { bodyBg: s.backgroundColor, bodyColor: s.color };
    }""")
    print("body:", probe)

    b.close()

