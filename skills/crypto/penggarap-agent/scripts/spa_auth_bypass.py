# Metadata: Origin Domain: kaito.ai, Date: 2026-08-21, Symptom: SPA React auth/X connect failure

async def force_click_auth_button(page, selector: str, timeout: int = 5000):
    """
    Force clicks auth buttons (Email/X) bypassing transparent overlays or pointer-events:none.
    """
    try:
        await page.wait_for_selector(selector, state='attached', timeout=timeout)
        await page.evaluate("(sel) => { const el = document.querySelector(sel) || document.evaluate(sel, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (el) el.click(); }", selector)
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
