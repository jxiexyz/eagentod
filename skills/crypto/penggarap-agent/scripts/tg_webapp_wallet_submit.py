# Metadata: Origin: puffins.fun, Date: 2026-08-22, Symptom: Element interaction blocked by TG WebApp iframe or generic wallet submission failure.
import asyncio
import re

async def bypass_wallet_submission(page, wallet_address: str, iframe_selector: str = 'iframe'):
    '''
    Bypasses standard DOM barriers to find wallet input fields and submit buttons.
    Works across iframes and shadow DOMs.
    '''
    target_frame = page
    if iframe_selector:
        try:
            frame_element = await page.wait_for_selector(iframe_selector, timeout=5000)
            if frame_element:
                target_frame = await frame_element.content_frame() or page
        except Exception:
            pass

    input_selectors = [
        "input[placeholder*='address' i]",
        "input[placeholder*='wallet' i]",
        "input[placeholder*='BSC' i]",
        "input[placeholder*='0x' i]",
        "input[name*='address' i]",
        "input[id*='address' i]"
    ]
    
    input_locator = None
    for sel in input_selectors:
        locator = target_frame.locator(sel).first
        if await locator.count() > 0:
            input_locator = locator
            break
            
    if not input_locator:
        raise Exception('Could not find wallet input field.')

    await input_locator.fill(wallet_address)
    
    button_selectors = [
        "button:has-text('Submit')",
        "button:has-text('Save')",
        "button:has-text('Confirm')",
        "button[type='submit']",
        "div[role='button']:has-text('Submit')"
    ]
    
    button_locator = None
    for sel in button_selectors:
        locator = target_frame.locator(sel).first
        if await locator.count() > 0:
            button_locator = locator
            break
            
    if button_locator:
        await button_locator.click()
    else:
        await input_locator.press('Enter')
        
    return True