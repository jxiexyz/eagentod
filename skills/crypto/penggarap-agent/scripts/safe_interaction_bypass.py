# Metadata: Origin Domain: app.rally.fun | Date: 2026-08-17 | Symptom: hermes -z no final response (hang/timeout on dynamic Web3 UI)
import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def safe_click(page: Page, selector: str, timeout: int = 5000) -> bool:
    """Attempts to click an element, falling back to JS evaluation to bypass shadow DOM/overlays and pointer-events blocks."""
    try:
        element = page.locator(selector).first
        await element.wait_for(state="visible", timeout=timeout)
        # Force click bypasses actionability checks that often hang in Web3 SPAs
        await element.click(timeout=timeout, force=True)
        return True
    except PlaywrightTimeoutError:
        try:
            js_click = f"""
            (() => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.click();
                    return true;
                }}
                return false;
            }})();
            """
            result = await page.evaluate(js_click)
            return bool(result)
        except Exception as e:
            print(f"Bypass JS fallback failed for {selector}: {e}")
            return False
    except Exception as e:
        print(f"Unexpected error clicking {selector}: {e}")
        return False

async def safe_wait_and_click(page: Page, selector: str, max_retries: int = 3, delay: int = 2) -> bool:
    for i in range(max_retries):
        if await safe_click(page, selector):
            return True
        await asyncio.sleep(delay)
    return False
