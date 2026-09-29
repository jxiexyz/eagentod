# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-22, Symptom: OAuth popup handling failures for X and GitHub during registration
import asyncio
from playwright.async_api import Page

async def handle_oauth_popup(page: Page, trigger_selector: str, provider: str = "x"):
    """
    Handles OAuth popups by waiting for the new page event when the trigger selector is clicked.
    provider: 'x' (Twitter) or 'github'
    """
    context = page.context
    async with context.expect_page() as popup_info:
        await page.click(trigger_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state("networkidle")
    
    if provider in ["x", "twitter"]:
        authorize_btn = "button[data-testid='OAuth_Consent_Button']"
        await popup.wait_for_selector(authorize_btn, state="visible", timeout=10000)
        await popup.click(authorize_btn)
    elif provider == "github":
        authorize_btn = "button[name='authorize']"
        try:
            await popup.wait_for_selector(authorize_btn, state="visible", timeout=10000)
            await popup.click(authorize_btn)
        except Exception:
            pass # Might already be authorized
    
    try:
        await popup.wait_for_event("close", timeout=15000)
    except Exception:
        if not popup.is_closed():
            await popup.close()
