# Metadata: Domain: app.gyndore.com, Date: 2026-08-26, Symptom: Shadow DOM or React Portals blocking Wallet/X connect clicks
import asyncio
from playwright.async_api import Page

async def bypass_shadow_dom_click(page: Page, selector: str, text_match: str = None, timeout_ms: int = 5000):
    """
    Finds and clicks an element piercing through Shadow DOMs.
    Useful for Privy, Web3Modal, and Dynamic.xyz overlays.
    """
    js_code = """
    ([sel, txt]) => {
        function pierce(root) {
            let found = root.querySelector(sel);
            if (found && (!txt || found.textContent.includes(txt))) return found;
            let el = root.firstElementChild;
            while (el) {
                if (el.shadowRoot) {
                    let shadowFound = pierce(el.shadowRoot);
                    if (shadowFound) return shadowFound;
                }
                let childFound = pierce(el);
                if (childFound) return childFound;
                el = el.nextElementSibling;
            }
            return null;
        }
        let el = pierce(document);
        if (el) {
            el.click();
            return true;
        }
        return false;
    }
    """
    end_time = asyncio.get_event_loop().time() + (timeout_ms / 1000.0)
    while asyncio.get_event_loop().time() < end_time:
        clicked = await page.evaluate(js_code, [selector, text_match])
        if clicked:
            return True
        await asyncio.sleep(0.5)
    return False