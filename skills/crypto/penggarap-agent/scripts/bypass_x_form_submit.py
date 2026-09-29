# Origin Domain: inkclub.club
# Date: 2026-08-24
# Symptom: Generic failure handling X follow/repost and EVM input form submission.

import asyncio
from playwright.async_api import Page

async def bypass_x_actions_and_submit(page: Page, address: str, action_selectors: list, input_selector: str, submit_selector: str):
    for sel in action_selectors:
        for el in await page.locator(sel).all():
            if await el.is_visible():
                await el.click(force=True)
                await asyncio.sleep(1.5)
    
    evm_field = page.locator(input_selector).first
    await evm_field.wait_for(state="visible", timeout=5000)
    await evm_field.fill(address)
    
    await page.locator(submit_selector).first.click(force=True)
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except:
        pass
    return True
