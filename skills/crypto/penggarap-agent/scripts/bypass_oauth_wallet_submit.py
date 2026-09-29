# Metadata: robinex.app, 2026-08-23, X OAuth popup context loss and wallet submission failure

async def handle_oauth_and_submit(page, connect_btn_selector: str, wallet_selector: str, wallet_address: str, submit_btn_selector: str):
    """Handles X OAuth popup window closing gracefully before filling the wallet."""
    # 1. Intercept popup
    async with page.expect_popup() as popup_info:
        await page.locator(connect_btn_selector).click()
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    # 2. Click 'Authorize app' if required by X
    auth_btn = popup.locator('[data-testid="OAuth_Consent_Button"]')
    try:
        await auth_btn.wait_for(state='visible', timeout=8000)
        await auth_btn.click()
    except Exception:
        pass  # Already authorized or auto-redirecting
        
    # 3. Wait for popup to safely close, return to main page
    try:
        await popup.wait_for_event('close', timeout=15000)
    except Exception:
        pass

    await page.bring_to_front()
    
    # 4. Fill wallet and submit
    wallet_field = page.locator(wallet_selector)
    await wallet_field.wait_for(state='visible', timeout=10000)
    await wallet_field.fill(wallet_address)
    
    await page.locator(submit_btn_selector).click()
    return True
