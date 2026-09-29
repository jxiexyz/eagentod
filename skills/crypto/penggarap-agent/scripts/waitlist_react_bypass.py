# Origin Domain: teogiwa.com
# Date: 2026-08-23
# Specific Symptom: Web automation fails to submit EVM address because standard fill() does not trigger React synthetic events or state updates.

async def fill_react_input(page, selector: str, value: str):
    """Fills an input field bypassing React event blockers by simulating physical keystrokes."""
    element = await page.wait_for_selector(selector, state="visible", timeout=10000)
    if not element:
        return False
        
    await element.click()
    # Select all and delete to clear existing text safely
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    
    # Type sequentially to trigger onChange handlers
    await element.type(value, delay=50)
    return True

async def submit_waitlist(page, input_selector: str, submit_selector: str, evm_address: str):
    """Generic waitlist submitter handling React forms."""
    input_filled = await fill_react_input(page, input_selector, evm_address)
    if not input_filled:
        return False
        
    btn = await page.wait_for_selector(submit_selector, state="visible", timeout=5000)
    if btn:
        await btn.click()
        await page.wait_for_load_state("networkidle", timeout=5000)
        return True
        
    return False
