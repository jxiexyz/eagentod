# Metadata: Origin Domain: testnet.x1ecochain.com, Date: 2026-08-25, Symptom: Waitlist EVM address submission blocked by pending dummy tasks and popup interruptions
import asyncio
from playwright.async_api import Page

async def bypass_waitlist_tasks_and_submit(page: Page, evm_address: str, task_selectors: list = None, input_selector: str = "input[placeholder*='0x' i], input[placeholder*='address' i]", submit_selector: str = "button:has-text('Submit' i), button:has-text('Join' i)"):
    if task_selectors is None:
        task_selectors = ["a[href*='twitter.com']", "a[href*='t.me']", "button:has-text('Verify' i)", "button:has-text('Follow' i)"]
    
    # Intercept and block window.open to prevent popup navigation hangs
    await page.evaluate("window.open = function() { return null; }")
    
    for selector in task_selectors:
        elements = await page.locator(selector).all()
        for el in elements:
            if await el.is_visible():
                try:
                    # Force enable disabled buttons and fix pointer events
                    await el.evaluate("node => { node.removeAttribute('disabled'); node.style.pointerEvents = 'auto'; }")
                    await el.click(force=True)
                    await asyncio.sleep(1.5)
                except Exception:
                    pass
    
    address_input = page.locator(input_selector).first
    if await address_input.count() > 0:
        await address_input.fill(evm_address)
        
        submit_btn = page.locator(submit_selector).first
        if await submit_btn.count() > 0:
            await submit_btn.evaluate("node => { node.removeAttribute('disabled'); node.style.pointerEvents = 'auto'; }")
            await submit_btn.click(force=True)
            await asyncio.sleep(2)
            
    return True
