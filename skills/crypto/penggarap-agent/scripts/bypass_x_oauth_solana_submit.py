# Metadata: Origin Domain: register.divvy.bet | Date: 2026-08-23 | Symptom: X OAuth popup block and wallet submission timeout
import asyncio
from playwright.async_api import Page

async def bypass_x_oauth_and_submit_wallet(
    page: Page,
    x_button_selector: str = "button:has-text('Connect X')",
    wallet_input_selector: str = "input[placeholder*='Solana']",
    submit_button_selector: str = "button:has-text('Submit')",
    solana_address: str = ""
) -> bool:
    """
    Handles X OAuth popup and submits a Solana wallet address generically.
    """
    try:
        # 1. Handle X OAuth Popup
        async with page.expect_popup() as popup_info:
            await page.click(x_button_selector)
        
        popup = await popup_info.value
        await popup.wait_for_load_state("networkidle")
        
        # Click authorize app on X.com (Twitter OAuth standard testid)
        auth_button = popup.locator("div[data-testid='OAuth_Consent_Button']")
        if await auth_button.is_visible(timeout=5000):
            await auth_button.click()
        
        # Wait for popup to close and main page to process
        await popup.wait_for_event("close", timeout=15000)
        await page.wait_for_timeout(2000)

        # 2. Submit Solana Wallet
        if solana_address:
            await page.fill(wallet_input_selector, solana_address)
            await page.wait_for_timeout(500)
            await page.click(submit_button_selector)
            await page.wait_for_timeout(2000)

        return True
    except Exception as e:
        print(f"[!] Bypass failed: {str(e)}")
        return False
