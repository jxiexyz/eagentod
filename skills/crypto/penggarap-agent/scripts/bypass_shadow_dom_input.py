# Metadata: Domain app.bullchaintestnet.ai, Date 2026-09-03, Symptom Shadow DOM blocks standard Playwright locators

async def bypass_shadow_dom_input(page, selector: str, value: str):
    await page.evaluate("""([sel, val]) => {
        const find = (s, r=document) => {
            let e = r.querySelector(s);
            if(e) return e;
            for(let h of r.querySelectorAll('*')) {
                if(h.shadowRoot && (e = find(s, h.shadowRoot))) return e;
            }
        };
        const el = find(sel);
        if(el) {
            el.value = val;
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }""", [selector, value])
