# Origin Domain: rpg.cash
# Date: 2026-08-27
# Specific Symptom: Failed to locate and submit EVM address in React/Custom UI forms

import asyncio

async def submit_evm_address(page, address: str, input_selector: str = 'input[placeholder*="0x"], input[placeholder*="Address"], input[type="text"]', submit_selector: str = 'button:has-text("Submit"), button:has-text("Confirm"), button:has-text("Summon")'):
    """Fills an EVM address into a generic input and submits it, with fallback to Enter key."""
    try:
        input_locator = page.locator(input_selector).first
        await input_locator.wait_for(state="visible", timeout=10000)
        
        await input_locator.focus()
        await input_locator.fill(address)
        await page.keyboard.press('Tab')
        
        await asyncio.sleep(1)
        
        submit_locator = page.locator(submit_selector).first
        if await submit_locator.is_visible():
            await submit_locator.click()
        else:
            await page.keyboard.press('Enter')
            
        await asyncio.sleep(2)
        return True
    except Exception as e:
        print(f"EVM submission bypass failed: {e}")
        return False
