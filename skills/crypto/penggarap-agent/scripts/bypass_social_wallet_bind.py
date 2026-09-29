# Metadata: Origin: register.divvy.bet | Date: 2026-08-23 | Symptom: X account bind and SOL wallet connection popup hang during registration
import asyncio

async def run_bypass(page, x_selector="text=/twitter|bind x/i", wallet_selector="text=/connect wallet/i", solana_selector="text=/phantom|solana/i"):
    try:
        async with page.expect_popup(timeout=10000) as popup_info:
            await page.locator(x_selector).first.click()
        popup = await popup_info.value
        await popup.wait_for_load_state('networkidle')
        auth_btn = popup.locator("text=/authorize app/i")
        if await auth_btn.is_visible():
            await auth_btn.click()
        if not popup.is_closed():
            await popup.close()
    except Exception as e:
        print(f"X bind step bypassed/failed: {e}")

    try:
        await page.locator(wallet_selector).first.click()
        sol_btn = page.locator(solana_selector).first
        if await sol_btn.is_visible(timeout=5000):
            await sol_btn.click()
        await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"Wallet connect bypassed/failed: {e}")

    return True
