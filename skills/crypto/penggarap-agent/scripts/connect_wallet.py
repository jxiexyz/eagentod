# Metadata: Domain: app.stabilizer.finance, Date: 2026-08-23, Symptom: Wallet connection modal bypass needed for profile claim

async def connect_web3_wallet(page, main_button_selector="button:has-text('Connect')"):
    try:
        if await page.locator(main_button_selector).is_visible():
            await page.click(main_button_selector)
            await page.wait_for_timeout(1000)
            
        wallet_options = [
            "button:has-text('MetaMask')",
            "button:has-text('Injected')",
            "button:has-text('Browser Wallet')",
            "[data-testid='rk-wallet-option-metaMask']"
        ]
        
        for sel in wallet_options:
            if await page.locator(sel).first.is_visible():
                await page.locator(sel).first.click()
                break
                
        await page.wait_for_timeout(2000)
        return True
    except Exception as e:
        print(f"Wallet connection failed: {e}")
        return False
