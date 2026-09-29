# Metadata: Domain: Generic/Rally.fun, Date: 2026-08-22, Symptom: Fails to capture and interact with external X/GitHub OAuth popups
import asyncio

async def handle_oauth_popup(page, trigger_selector, timeout=30000):
    """Click a button that opens an OAuth popup and authorize it."""
    async with page.expect_popup(timeout=timeout) as popup_info:
        await page.click(trigger_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state("domcontentloaded")
    
    url = popup.url.lower()
    if "twitter.com" in url or "x.com" in url:
        auth_btn = popup.locator("[data-testid='OAuth_Consent_Button']")
        try:
            await auth_btn.wait_for(state="visible", timeout=10000)
            await auth_btn.click()
        except Exception:
            pass
    elif "github.com" in url:
        auth_btn = popup.locator("#js-oauth-authorize-btn, button[name='authorize']")
        try:
            await auth_btn.wait_for(state="visible", timeout=10000)
            await auth_btn.click()
        except Exception:
            pass
            
    try:
        await popup.wait_for_event("close", timeout=15000)
    except Exception:
        if not popup.is_closed():
            await popup.close()
