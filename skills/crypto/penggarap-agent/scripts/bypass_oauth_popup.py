# Metadata: Origin Domain: app.askoro.ai, Date: 2026-08-27, Symptom: Playwright hanging on external X/Twitter Connect OAuth popups during social tasks

import asyncio

async def bypass_oauth_popup(page, trigger_selector: str, auth_selector: str = "[data-testid='OAuth_Consent_Button']", timeout: int = 15000):
    """
    Clicks a trigger that opens an OAuth popup (like X/Twitter), switches to it, and authorizes.
    """
    async with page.expect_popup(timeout=timeout) as popup_info:
        await page.click(trigger_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state("domcontentloaded")
    
    try:
        await popup.wait_for_selector(auth_selector, state="visible", timeout=timeout)
        await popup.click(auth_selector)
        # Wait for the popup to process and close itself automatically after authorization
        await popup.wait_for_event("close", timeout=timeout)
        return True
    except Exception as e:
        print(f"Popup auth failed or closed early: {e}")
        if not popup.is_closed():
            await popup.close()
        return False
