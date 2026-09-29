# Metadata: Origin Domain: Generic Waitlist (ink-ape.xyz)
# Date: 2026-08-25
# Symptom: Form submission failure due to React synthetic events or obscured generic selectors

import asyncio

async def fill_and_submit_evm(page, evm_address: str, input_locator: str = None, submit_locator: str = None):
    """
    Bypasses React synthetic event blocking by realistically typing the EVM address and submitting.
    """
    inputs = input_locator or 'input[placeholder*="0x" i], input[placeholder*="address" i], input[type="text"]'
    buttons = submit_locator or 'button:has-text("Join" i), button:has-text("Submit" i), button:has-text("Enter" i)'

    input_el = page.locator(inputs).first
    await input_el.wait_for(state="visible", timeout=15000)
    
    # Realistic typing to trigger React/Vue onChange handlers
    await input_el.focus()
    await input_el.fill("")
    await input_el.type(evm_address, delay=50)

    # Allow framework validation state to catch up before clicking
    await asyncio.sleep(1)

    btn_el = page.locator(buttons).first
    await btn_el.wait_for(state="visible", timeout=5000)
    await btn_el.click()
    
    try:
        await page.wait_for_timeout(3000) # Wait for success toast, network idle, or redirect
    except Exception:
        pass
        
    return True
