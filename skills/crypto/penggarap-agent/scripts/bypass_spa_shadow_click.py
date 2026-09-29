# Metadata: app.allscale.io, 2026-08-24, Element not interactable / Shadow DOM boundary
import asyncio

async def execute(page, selector, text_fallback=None, timeout=15000):
    """
    Bypass for slow-rendering SPAs and Shadow DOM barriers.
    Attempts native click, falls back to JS DOM evaluation.
    """
    try:
        element = await page.wait_for_selector(selector, state='visible', timeout=timeout)
        if element:
            await element.scroll_into_view_if_needed()
            await asyncio.sleep(0.5)
            await element.click()
            return True
    except Exception:
        pass

    js_script = """(sel, txt) => {
        function findEl(root) {
            let el = root.querySelector(sel);
            if (el && (!txt || el.innerText.includes(txt))) return el;
            for (let child of root.querySelectorAll('*')) {
                if (child.shadowRoot) {
                    let inner = findEl(child.shadowRoot);
                    if (inner) return inner;
                }
            }
            return null;
        }
        let target = findEl(document);
        if (target) {
            target.click();
            return true;
        }
        return false;
    }"""
    
    success = await page.evaluate(js_script, selector, text_fallback)
    if not success:
        raise Exception(f"Bypass failed: Could not locate or click {selector}")
    return True
