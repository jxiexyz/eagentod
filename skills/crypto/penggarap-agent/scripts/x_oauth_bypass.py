# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-22, Symptom: X OAuth popup handling and authorization click failure

import asyncio
from playwright.async_api import Page

async def bypass_x_oauth(page: Page, login_selector: str) -> bool:
    """
    Generic bypass for X (Twitter) OAuth flows. Handles both popup windows and direct redirects,
    clicking the authorization consent button automatically.
    """
    try:
        # Anticipate a popup window for OAuth
        async with page.expect_event("popup", timeout=8000) as popup_info:
            await page.locator(login_selector).first.click()
        
        target_page = await popup_info.value
        await target_page.wait_for_load_state("domcontentloaded")
    except Exception:
        # Fallback to same-tab redirect if popup listener times out
        await page.locator(login_selector).first.click()
        await page.wait_for_url(lambda url: "api.x.com/oauth" in url or "twitter.com/i/oauth2" in url, timeout=10000)
        target_page = page

    # Wait for and click the 'Authorize app' button on X
    auth_btn = target_page.locator("button[data-testid='OAuth_Consent_Button'], input#allow, [data-testid='allow']")
    await auth_btn.wait_for(state="visible", timeout=15000)
    await auth_btn.click()

    # If popup, wait for it to close and return control
    if target_page != page:
        try:
            await target_page.wait_for_event("close", timeout=15000)
        except Exception:
            pass # Might already be closed or redirected internally

    return True
