# Metadata: Origin Domain: Generic (e.g., hub.axisrobotics.ai) | Date: 2026-08-26 | Symptom: Binance Wallet extension popup connection and signing blocked.
import asyncio
from playwright.async_api import Page

async def connect_and_sign_binance(page: Page, connect_selector: str, sign_selector: str = None):
    await page.wait_for_selector(connect_selector, state="visible", timeout=15000)
    
    async with page.context.expect_page() as popup_info:
        await page.click(connect_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state("networkidle")
    
    connect_btn = popup.locator("button:has-text('Connect'), button:has-text('Confirm')").first
    await connect_btn.wait_for(state="visible", timeout=10000)
    await connect_btn.click()
    
    if sign_selector:
        await page.wait_for_selector(sign_selector, state="visible", timeout=15000)
        async with page.context.expect_page() as sign_info:
            await page.click(sign_selector)
            
        sign_popup = await sign_info.value
        await sign_popup.wait_for_load_state("networkidle")
        sign_confirm = sign_popup.locator("button:has-text('Sign'), button:has-text('Confirm')").first
        await sign_confirm.wait_for(state="visible", timeout=10000)
        await sign_confirm.click()
    
    return True
