# Metadata: Domain: inkpunk.xyz, Date: 2026-08-24, Symptom: Social tasks hang and EVM address input React state failure
import asyncio

async def solve_whitelist_form(page, evm_address: str, social_btn_selector: str = "button:has-text('Follow'), button:has-text('Verify')", input_selector: str = "input[type='text']", submit_selector: str = "button:has-text('Submit')"):
    # Click social buttons to trigger any local verification state
    social_btns = await page.locator(social_btn_selector).all()
    for btn in social_btns:
        if await btn.is_visible():
            await btn.click(force=True)
            await page.wait_for_timeout(1000)
    
    # Fill EVM input and force React state update
    target_input = page.locator(input_selector).first
    if await target_input.is_visible():
        await target_input.fill(evm_address)
        # Dispatch native events to bypass React synthetic event blockers
        await target_input.evaluate('node => node.dispatchEvent(new Event("input", { bubbles: true }))')
        await target_input.evaluate('node => node.dispatchEvent(new Event("change", { bubbles: true }))')
        await page.wait_for_timeout(500)
    
    # Click Submit
    submit_btn = page.locator(submit_selector).first
    if await submit_btn.is_visible():
        await submit_btn.click(force=True)
        await page.wait_for_timeout(2000)
    
    return True
