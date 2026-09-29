# Origin Domain: sohonft.site
# Date: 2026-08-21
# Symptom: Click intercepted by overlay or element not interactable during whitelist registration.

import asyncio
from playwright.async_api import Page

async def bypass_click_intercept(page: Page, selector: str, timeout: int = 5000):
    """
    Attempts to click an element, falling back to JS click if intercepted by an overlay.
    """
    try:
        element = page.locator(selector).first
        await element.wait_for(state="visible", timeout=timeout)
        await element.scroll_into_view_if_needed()
        await element.click(timeout=timeout)
    except Exception as e:
        if "intercepted" in str(e).lower() or "not interactable" in str(e).lower():
            # Fallback to JS evaluation click to bypass DOM overlays
            await page.evaluate("(sel) => { const el = document.querySelector(sel); if(el) el.click(); }", selector)
        else:
            raise e
