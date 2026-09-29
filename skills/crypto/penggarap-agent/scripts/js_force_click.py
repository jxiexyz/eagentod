# Metadata: Domain: Generic (Target: chatlee.io), Date: 2026-08-21, Symptom: Element interception / Unknown interaction failure (session: 20260821_042410_221c0a)

async def force_click(page, selector: str, timeout: int = 5000):
    """
    Bypasses Playwright element interception and shadow DOM blocks by executing a raw JS click.
    """
    try:
        await page.wait_for_selector(selector, state='attached', timeout=timeout)
        await page.evaluate(f"(sel) => document.querySelector(sel)?.click()", selector)
        return True
    except Exception as e:
        print(f"Bypass force click failed for {selector}: {e}")
        return False
