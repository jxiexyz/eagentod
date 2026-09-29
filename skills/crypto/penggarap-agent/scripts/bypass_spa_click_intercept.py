# Metadata: sheeps.ink, 2026-08-25, Playwright click interception on SPA quest buttons
import asyncio

async def bypass_click_intercept(page, selector: str, timeout: int = 5000):
    """
    Force dispatch of MouseEvents to bypass pointer-events:none or overlapping overlays in SPAs.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.evaluate("""(sel) => {
            const el = document.querySelector(sel);
            if (el) {
                el.scrollIntoView({ behavior: 'smooth', block: 'center' });
                ['mouseover', 'mousedown', 'mouseup', 'click'].forEach(ev => 
                    el.dispatchEvent(new MouseEvent(ev, { bubbles: true, cancelable: true, view: window }))
                );
            }
        }""", selector)
        return True
    except Exception as e:
        print(f"[Bypass] Click failed for {selector}: {e}")
        return False
