# Metadata: Domain: inklords.xyz, Date: 2026-08-24, Symptom: Whitelist form EVM submission failure
import asyncio
from playwright.async_api import Page

async def bypass_evm_whitelist_form(page: Page, wallet_address: str, submit_keyword: str = 'Submit'):
    input_selector = "input[placeholder*='0x'], input[name*='wallet' i], input[name*='address' i]"
    submit_selector = f"button:has-text('{submit_keyword}'), button[type='submit'], input[type='submit']"
    
    await page.wait_for_selector(input_selector, state='visible', timeout=10000)
    inputs = await page.locator(input_selector).all()
    
    for el in inputs:
        if await el.is_visible() and not await el.is_disabled():
            await el.fill(wallet_address)
            break
            
    await asyncio.sleep(1)
    
    submit_btn = page.locator(submit_selector).first
    if await submit_btn.is_visible():
        await submit_btn.click()
        await page.wait_for_load_state('networkidle', timeout=10000)
        return True
    return False
