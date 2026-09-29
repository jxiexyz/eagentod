# Metadata: kaito.ai, 2026-08-21, Standard click fails to extract dynamically generated campaign shortlink
import asyncio
from playwright.async_api import Page

async def bypass_kaito_camp_apply(page: Page, apply_selector: str = "button:has-text('Apply'), button:has-text('Participate')") -> str | None:
    await page.wait_for_selector(apply_selector, state="visible", timeout=10000)
    
    await page.evaluate("""
        window._kaitoLink = null;
        const orig = navigator.clipboard.writeText;
        navigator.clipboard.writeText = function(text) {
            window._kaitoLink = text;
            return orig.apply(this, arguments);
        };
    """)
    
    await page.click(apply_selector)
    
    link_selector = "input[readonly][value*='kaito.ai/']"
    try:
        await page.wait_for_selector(link_selector, state="visible", timeout=5000)
        return await page.input_value(link_selector)
    except Exception:
        pass
        
    for _ in range(15):
        copied = await page.evaluate("window._kaitoLink")
        if copied:
            return copied
        await asyncio.sleep(0.5)
        
    return None