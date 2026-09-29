# Metadata: Origin Domain: octra.fun, Date: 2026-08-25, Symptom: Complex waitlist submission requiring task completion, access code (kode aksara), and EVM address.
import asyncio
from playwright.async_api import Page

async def process_waitlist_tasks(page: Page, evm_address: str, access_code: str = "", evm_sel: str = "input[placeholder*='0x'], input[name*='wallet'], input[placeholder*='EVM' i]", code_sel: str = "input[placeholder*='code' i], input[placeholder*='aksara' i], input[name*='code' i]", task_btn_sel: str = "button:has-text('Verify'), button:has-text('Follow'), button:has-text('Go'), button:has-text('Start')"):
    """
    Generic handler for web3 waitlists requiring sequential task verification, access codes, and EVM addresses.
    """
    try:
        # 1. Input Access/Aksara Code
        if access_code:
            code_inputs = await page.locator(code_sel).all()
            for inp in code_inputs:
                if await inp.is_visible():
                    await inp.fill(access_code)
                    break
                
        # 2. Iterate and Complete Tasks (Verify/Follow buttons)
        task_buttons = await page.locator(task_btn_sel).all()
        for btn in task_buttons:
            if await btn.is_visible() and not await btn.is_disabled():
                await btn.click()
                # Brief pause to allow popups or state changes to register
                await asyncio.sleep(2.0) 
                
        # 3. Input EVM Address
        evm_inputs = await page.locator(evm_sel).all()
        for inp in evm_inputs:
            if await inp.is_visible():
                await inp.fill(evm_address)
                break
                
        # 4. Submit Form
        submit_btn = page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Join Waitlist'), button:has-text('Register')").first
        if await submit_btn.is_visible():
            await submit_btn.click()
            
        # Allow network requests to resolve post-submission
        try:
            await page.wait_for_load_state("networkidle", timeout=5000)
        except:
            pass # Ignore timeout if network isn't fully idle but click registered
            
        return {"status": "success", "message": "Waitlist tasks processed and submitted."}
    except Exception as e:
        return {"status": "error", "message": f"Waitlist submission bypass failed: {str(e)}"}
