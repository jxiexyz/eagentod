# Metadata: Origin Domain: sheeps.ink, Date: 2026-08-25, Symptom: Playwright element intercepted or strict visibility checks failing on custom UI overlays.

async def force_js_click(page, selector: str, timeout: int = 10000):
    """
    Forces a native browser click via JS, bypassing Playwright's actionability checks.
    Useful for overlapping crypto overlays or React portals blocking standard clicks.
    """
    locator = page.locator(selector).first
    await locator.wait_for(state="attached", timeout=timeout)
    await locator.evaluate("node => node.click()")
    return True
