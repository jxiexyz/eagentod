# Metadata: Origin Domain: memebitcoin.org | Date: 2026-08-24 | Symptom: Social account connection popup/timeout failure during whitelist registration.

import asyncio

async def handle_social_connect(page, trigger_selector: str, auth_selector: str = None, timeout: int = 15000):
    """
    Generic handler for social (X/Discord) OAuth popups.
    Clicks trigger on main page, waits for popup, clicks auth button inside popup.
    """
    try:
        async with page.context.expect_page(timeout=timeout) as popup_info:
            await page.locator(trigger_selector).wait_for(state='visible', timeout=timeout)
            await page.locator(trigger_selector).click()
        
        popup = await popup_info.value
        await popup.wait_for_load_state('networkidle')
        
        if auth_selector:
            await popup.locator(auth_selector).wait_for(state='visible', timeout=timeout)
            await popup.locator(auth_selector).click()
            
        # Wait for the auth flow to close the popup
        await popup.wait_for_event('close', timeout=timeout * 2)
        return True
    except Exception as e:
        print(f"Social connect failed: {e}")
        return False
