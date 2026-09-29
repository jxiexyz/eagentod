# Metadata: Origin Domain: generic (etherbubu.com), Date: 2026-08-21, Symptom: X/Twitter OAuth popup window blocks execution or gets lost in context.

import asyncio

async def handle_oauth_popup(page, trigger_selector: str, auth_btn_selector: str = "[data-testid='OAuth_Consent_Button']"):
    """Handles OAuth popups (e.g., X connection) cleanly."""
    try:
        async with page.context.expect_page(timeout=10000) as popup_info:
            await page.locator(trigger_selector).click(force=True)
        
        popup = await popup_info.value
        await popup.wait_for_load_state("domcontentloaded")
        
        auth_btn = popup.locator(auth_btn_selector)
        if await auth_btn.count() > 0:
            await auth_btn.click()
            
        try:
            await popup.wait_for_event("close", timeout=15000)
        except Exception:
            pass
            
        if not popup.is_closed():
            await popup.close()
            
    except Exception as e:
        print(f"Popup bypass failed: {e}")
        
    return page