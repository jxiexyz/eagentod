# Metadata: Origin Domain: digitsbt.ngrndrewards.com, Date: 2026-08-24, Symptom: General EVM address form submission failure
import asyncio
from playwright.async_api import Page

async def submit_evm_address(page: Page, address: str, input_selector: str = None, submit_selector: str = None):
    """Generic bypass for React/Shadow DOM EVM address forms."""
    if not input_selector:
        input_selector = 'input[placeholder*="0x" i], input[placeholder*="address" i], input[name*="wallet" i], input[type="text"]'
    if not submit_selector:
        submit_selector = 'button:has-text("Submit"), button:has-text("Apply"), button:has-text("Join"), button:has-text("Claim")'

    input_locator = page.locator(input_selector).first
    await input_locator.wait_for(state="visible", timeout=15000)
    await input_locator.fill(address)
    await input_locator.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
    await input_locator.evaluate("el => el.dispatchEvent(new Event('change', { bubbles: true }))")
    await asyncio.sleep(1.2)

    submit_locator = page.locator(submit_selector).first
    await submit_locator.wait_for(state="visible", timeout=5000)
    await submit_locator.click(force=True)
    try:
        await page.wait_for_load_state("networkidle", timeout=10000)
    except:
        pass
    return True
