# Metadata: Origin Domain: etherbubu.com | Date: 2026-08-21 | Symptom: FCFS claim button click intercepted or hidden by overlays

async def force_claim_click(page, selector: str):
    """
    Forces a click on an element, bypassing React synthetic event interception, 
    overlapping overlays, and shadow DOM issues.
    """
    try:
        # 1. Try native Playwright force click
        await page.locator(selector).click(force=True, timeout=5000)
        return True
    except Exception:
        # 2. Fallback to pure JS direct DOM manipulation
        js_script = """
        (sel) => {
            const el = document.querySelector(sel);
            if (el) {
                el.scrollIntoView({ behavior: 'instant', block: 'center' });
                el.click();
                return true;
            }
            return false;
        }
        """
        result = await page.evaluate(js_script, selector)
        return result
