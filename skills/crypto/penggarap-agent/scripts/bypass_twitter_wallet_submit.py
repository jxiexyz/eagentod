# Metadata: Origin Domain: robinex.app | Date: 2026-08-23 | Symptom: Fails to handle X/Twitter connect popup and wallet submission form.
import asyncio

async def run(page, x_auth_selector: str, wallet_input_selector: str, submit_selector: str, wallet_address: str):
    """
    Bypasses standard early-access flows requiring X connection and wallet submission.
    """
    try:
        # 1. Handle X connection (often triggers a popup)
        async with page.expect_popup(timeout=5000) as popup_info:
            await page.locator(x_auth_selector).click()
        popup = await popup_info.value
        await popup.wait_for_load_state('networkidle')
        
        # Authorize app if needed (assuming session is authenticated via cookies)
        auth_btn = popup.locator('button[data-testid="OAuth_Consent_Button"]')
        if await auth_btn.is_visible(timeout=5000):
            await auth_btn.click()
            
        await popup.wait_for_event('close', timeout=15000)
    except Exception:
        # Fallback if it's a redirect instead of a popup or already connected
        print("No popup detected or already connected. Proceeding on main page.")
        if await page.locator(x_auth_selector).is_visible():
            await page.locator(x_auth_selector).click()
            await page.wait_for_load_state('networkidle')

    # 2. Fill wallet address
    await page.wait_for_selector(wallet_input_selector, state='visible', timeout=10000)
    await page.locator(wallet_input_selector).fill(wallet_address)

    # 3. Submit
    await page.locator(submit_selector).click()
    await page.wait_for_load_state('networkidle')
    
    return True
