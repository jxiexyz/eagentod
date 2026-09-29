# Metadata: cyro.global, 2026-08-27, Quest platform OAuth and Wallet Connect sequence timeout
import asyncio

async def handle_oauth_and_wallet(page, auth_btn_selectors: list, wallet_btn_selector: str):
    """
    Handles sequential OAuth popups (Google/X) and Web3 Wallet connect dialogs.
    """
    for selector in auth_btn_selectors:
        try:
            await page.wait_for_selector(selector, state='visible', timeout=5000)
            
            async with page.expect_popup() as popup_info:
                await page.click(selector)
            popup = await popup_info.value
            await popup.wait_for_load_state('networkidle')
            
            # Auto-approve common OAuth prompts if visible
            approve_btns = popup.locator('button:has-text("Authorize"), button:has-text("Allow"), button:has-text("Continue")')
            if await approve_btns.count() > 0:
                await approve_btns.first.click()
                
        except Exception as e:
            print(f"OAuth step failed for {selector}: {e}")
            continue

    # Wallet connect phase
    try:
        if wallet_btn_selector:
            await page.wait_for_selector(wallet_btn_selector, state='visible', timeout=5000)
            await page.click(wallet_btn_selector)
            
            # Select injected wallet (e.g., Phantom) if popup modal appears
            injected_wallet = page.locator('button:has-text("Phantom"), button:has-text("Injected")')
            if await injected_wallet.is_visible(timeout=3000):
                await injected_wallet.first.click()
                
    except Exception as e:
        print(f"Wallet connect failed: {e}")
        
    return True
