# Metadata: Domain: pipkits.space, Date: 2026-08-26, Symptom: Element click intercepted by overlay / Timeout on whitelist form
import asyncio
from playwright.async_api import Page

async def force_click(page: Page, selector: str, max_retries: int = 3):
    """Bypasses standard click interceptions (e.g., transparent overlays, hydration delays) by falling back to JS evaluation."""
    for attempt in range(max_retries):
        try:
            el = page.locator(selector).first
            await el.wait_for(state='attached', timeout=5000)
            await el.click(timeout=3000)
            return True
        except Exception as e:
            try:
                await el.evaluate('el => el.click()')
                return True
            except Exception:
                if attempt == max_retries - 1:
                    raise e
                await asyncio.sleep(1)
    return False