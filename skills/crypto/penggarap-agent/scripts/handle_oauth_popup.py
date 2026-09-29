# Metadata: mudlarknft.com, 2026-08-21, X/Twitter OAuth popup interaction failure

import asyncio

async def handle_popup_auth(page, trigger_selector: str, auth_confirm_selector: str = "[data-testid='OAuth_Consent_Button']"):
    """
    Handles clicking a button that opens an OAuth popup, interacting with the popup, 
    and waiting for it to close successfully.
    """
    try:
        async with page.expect_popup() as popup_info:
            await page.locator(trigger_selector).click()
        popup = await popup_info.value
        await popup.wait_for_load_state('domcontentloaded')
        
        if auth_confirm_selector:
            await popup.wait_for_selector(auth_confirm_selector, state='visible', timeout=15000)
            await popup.locator(auth_confirm_selector).click()
            
        await popup.wait_for_event('close', timeout=30000)
        return True
    except Exception as e:
        print(f"Popup auth bypass failed: {e}")
        return False