# Metadata: sheeps.ink, 2026-08-25, Playwright click intercepted/ignored by React synthetic events
import asyncio

async def force_react_click(page, selector: str, timeout: int = 5000):
    """
    Bypasses Playwright's strict actionability checks by dispatching native MouseEvents.
    Useful for Web3 frontends with complex overlays or custom React event handlers.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        await page.evaluate('''async (sel) => {
            const el = document.querySelector(sel);
            if (!el) throw new Error("Element not found");
            const events = ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'];
            for (const ev of events) {
                el.dispatchEvent(new MouseEvent(ev, { bubbles: true, cancelable: true, view: window }));
                await new Promise(r => setTimeout(r, 50));
            }
        }''', selector)
        return True
    except Exception as e:
        print(f"Bypass click failed for {selector}: {e}")
        return False
