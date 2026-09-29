# Metadata:
# Origin Domain: register.divvy.bet
# Date: 2026-08-23
# Symptom: Hangs on X OAuth popup window or fails to fire React state on wallet input.

import asyncio

async def bypass(page, x_connect_selector, wallet_input_selector, submit_selector, wallet_address):
    # 1. Handle X OAuth Popup
    async with page.context.expect_page() as popup_info:
        await page.locator(x_connect_selector).click()
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    try:
        auth_btn = popup.locator('[data-testid="OAuth_Consent_Button"]')
        await auth_btn.wait_for(state="visible", timeout=8000)
        await auth_btn.click()
    except Exception:
        pass
        
    try:
        await popup.wait_for_event("close", timeout=15000)
    except Exception:
        pass
        
    # 2. Fill Wallet Address
    wallet_input = page.locator(wallet_input_selector)
    await wallet_input.wait_for(state="visible", timeout=10000)
    await wallet_input.fill(wallet_address)
    # Force React event via dispatch
    await wallet_input.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
    
    # 3. Submit
    await page.locator(submit_selector).click()
    return True
