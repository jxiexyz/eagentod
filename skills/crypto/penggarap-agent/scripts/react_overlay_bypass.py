# Metadata: Domain: app.rally.fun, Date: 2026-08-26, Symptom: Element click intercepted / dynamic overlay blocking clicks.

async def force_click(page, selector, timeout=10000):
    """Force clicks an element via JS evaluation to bypass overlays."""
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.evaluate("([sel]) => { const el = document.querySelector(sel); if (el) { el.scrollIntoView({behavior: 'smooth', block: 'center'}); el.click(); } }", [selector])
        return True
    except Exception as e:
        print(f"Bypass click failed for {selector}: {e}")
        return False

async def force_click_text(page, text, timeout=10000):
    """Finds element containing text and force clicks it."""
    try:
        xpath = f"//*[contains(text(), '{text}')]"
        await page.wait_for_selector(xpath, state="attached", timeout=timeout)
        await page.evaluate("([xp]) => { const el = document.evaluate(xp, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue; if (el) { el.scrollIntoView({behavior: 'smooth', block: 'center'}); el.click(); } }", [xpath])
        return True
    except Exception as e:
        print(f"Bypass text click failed for '{text}': {e}")
        return False
