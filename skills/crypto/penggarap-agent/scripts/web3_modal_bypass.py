# Metadata: Domain: app.rally.fun, Date: 2026-08-26, Symptom: Web3 auth modal interaction failure

async def bypass_shadow_click(page, selector: str):
    js_script = """(sel) => {
        const find = (root) => root.querySelector(sel) || Array.from(root.querySelectorAll('*')).reduce((acc, el) => acc || (el.shadowRoot && find(el.shadowRoot)), null);
        const el = find(document);
        if (el) { el.click(); return true; }
        return false;
    }"""
    if not await page.evaluate(js_script, selector):
        raise ValueError(f"Selector {selector} not found in DOM or Shadow DOM")