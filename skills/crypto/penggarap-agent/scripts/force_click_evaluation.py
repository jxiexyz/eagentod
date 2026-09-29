# Metadata: Origin Domain: siloprotocol.xyz | Date: 2026-08-22 | Symptom: Element not interactable or click intercepted by overlays

async def force_click_element(page, selector: str):
    """
    Bypasses strict actionability checks by forcing a click directly via DOM evaluation.
    """
    try:
        await page.wait_for_selector(selector, state='attached', timeout=5000)
        await page.evaluate('(sel) => { const el = document.querySelector(sel); if (el) el.click(); }', selector)
        return True
    except Exception as e:
        print(f"Failed to force click {selector}: {e}")
        return False
