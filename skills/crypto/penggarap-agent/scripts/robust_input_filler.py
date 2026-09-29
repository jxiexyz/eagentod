# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-23, Symptom: Standard fill() fails or triggers bot detection on redeem inputs.
import asyncio
import random

async def fill_and_submit(page, input_selector: str, text: str, submit_selector: str = None):
    """Robustly fill an input and optionally click submit to bypass basic bot checks."""
    await page.wait_for_selector(input_selector, state='visible', timeout=10000)
    element = await page.locator(input_selector).first
    await element.scroll_into_view_if_needed()
    await element.click(delay=random.randint(50, 150))
    
    # Clear existing text
    await element.press('Control+A')
    await element.press('Backspace')
    
    # Human-like typing
    await element.type(text, delay=random.randint(100, 300))
    
    if submit_selector:
        await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
        submit_btn = await page.locator(submit_selector).first
        await submit_btn.scroll_into_view_if_needed()
        await asyncio.sleep(random.uniform(0.5, 1.5))
        await submit_btn.click(delay=random.randint(50, 150))
        try:
            await page.wait_for_load_state('networkidle', timeout=5000)
        except:
            pass
