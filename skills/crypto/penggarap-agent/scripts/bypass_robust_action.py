# Metadata: Origin Domain: fortunefoes.com | Date: 2026-08-25 | Symptom: Strict actionability check failure / Intercepted clicks on overlays
import asyncio

async def bypass_robust_action(page, selector: str, action: str = "click", text: str = None, timeout: int = 15000):
    """
    Executes clicks or fills bypassing Playwright's strict actionability checks.
    Useful for sites with heavy overlays, custom cursors, or shadow DOMs.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
        if action == "click":
            js_click = """(sel) => {
                const el = document.querySelector(sel);
                if (el) {
                    el.scrollIntoView({behavior: 'smooth', block: 'center'});
                    el.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
                }
            }"""
            await page.evaluate(js_click, selector)
        elif action == "fill" and text is not None:
            js_fill = """([sel, val]) => {
                const el = document.querySelector(sel);
                if (el) {
                    el.value = val;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }"""
            await page.evaluate(js_fill, [selector, text])
            
        await asyncio.sleep(1)
        return True
    except Exception as e:
        print(f"[Bypass] Failed {action} on {selector}: {e}")
        return False
