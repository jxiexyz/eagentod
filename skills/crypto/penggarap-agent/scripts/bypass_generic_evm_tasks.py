# Metadata: Origin Domain: theofficenft.io, Date: 2026-08-27, Symptom: Social task completion and EVM address submission failure
from playwright.async_api import Page

async def bypass_tasks_and_submit(page: Page, evm_address: str, tasks_sel="button:has-text('Verify'), button:has-text('Follow'), a:has-text('Join')", input_sel="input[placeholder*='0x'], input[name*='wallet']", submit_sel="button:has-text('Submit'), button:has-text('Enter')"):
    for btn in await page.locator(tasks_sel).all():
        if await btn.is_visible():
            await btn.click()
            await page.wait_for_timeout(1500)
    
    inp = page.locator(input_sel).first
    await inp.wait_for(state="visible", timeout=3000)
    await inp.fill(evm_address)
    
    sub = page.locator(submit_sel).first
    await sub.click()
    await page.wait_for_timeout(2000)
    return True