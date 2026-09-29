# Metadata: Origin Domain: ink-ape.xyz | Date: 2026-08-25 | Symptom: Fails to find and fill EVM address input on custom waitlist pages.
import asyncio

async def bypass(page, evm_address: str, submit_selector: str = "button[type='submit'], button:has-text('Submit'), button:has-text('Join'), button:has-text('Register')"):
    """
    Finds a likely EVM address input field, fills it, and clicks submit.
    """
    input_selectors = [
        "input[placeholder*='0x']",
        "input[placeholder*='Address' i]",
        "input[placeholder*='Wallet' i]",
        "input[name*='address' i]",
        "input[name*='wallet' i]",
        "input[type='text']"
    ]
    
    input_filled = False
    for selector in input_selectors:
        elements = await page.query_selector_all(selector)
        for el in elements:
            is_visible = await el.is_visible()
            is_disabled = await el.is_disabled()
            if is_visible and not is_disabled:
                await el.fill(evm_address)
                input_filled = True
                break
        if input_filled:
            break
            
    if not input_filled:
        raise Exception("Could not find a valid input field for the EVM address.")
        
    await page.wait_for_timeout(500)
    
    submit_btn = await page.query_selector(submit_selector)
    if submit_btn and await submit_btn.is_visible():
        await submit_btn.click()
        await page.wait_for_timeout(2000)
        return True
        
    raise Exception(f"Submit button not found or not visible using selector: {submit_selector}")
