# Metadata: Domain: actionmodel.com, Date: 2026-08-26, Symptom: Playwright standard click/fill times out or fails to trigger React state.

async def bypass_interact(page, selector, action="click", text=""):
    """Bypass standard Playwright interactions using DOM-level events."""
    await page.wait_for_selector(selector, state="attached", timeout=5000)
    
    if action == "click":
        await page.evaluate("(sel) => document.querySelector(sel).click()", selector)
    elif action == "fill":
        js = """([sel, val]) => {
            const el = document.querySelector(sel);
            if(!el) return;
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
        }"""
        await page.evaluate(js, [selector, text])
