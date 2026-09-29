# Origin Domain: playwithmimo.xyz
# Date: 2026-08-22
# Symptom: Failed to find and submit EVM address waitlist form.

import asyncio

async def run(page, evm_address: str):
    """
    Heuristically finds and fills EVM waitlist forms, bypassing rigid selectors.
    """
    input_selectors = [
        "input[placeholder*='0x' i]",
        "input[placeholder*='address' i]",
        "input[placeholder*='wallet' i]",
        "input[placeholder*='EVM' i]",
        "input[type='text']"
    ]
    
    filled = False
    for sel in input_selectors:
        try:
            inputs = await page.locator(sel).all()
            for input_loc in inputs:
                if await input_loc.is_visible() and not await input_loc.is_disabled():
                    await input_loc.fill(evm_address)
                    filled = True
                    break
            if filled:
                break
        except Exception:
            continue
            
    if not filled:
        raise Exception("Could not find a valid EVM address input field.")
        
    button_selectors = [
        "button:has-text('Submit')",
        "button:has-text('Join')",
        "button:has-text('Waitlist')",
        "button[type='submit']",
        "div[role='button']:has-text('Join')"
    ]
    
    clicked = False
    for sel in button_selectors:
        try:
            buttons = await page.locator(sel).all()
            for btn in buttons:
                if await btn.is_visible() and not await btn.is_disabled():
                    await btn.click()
                    clicked = True
                    break
            if clicked:
                break
        except Exception:
            continue
            
    if not clicked:
        raise Exception("Could not find a valid submit button.")
        
    try:
        await page.wait_for_load_state('networkidle', timeout=3000)
    except:
        pass
        
    return True
