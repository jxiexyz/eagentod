# Metadata: Origin Domain: chatlee.io, Date: 2026-08-21, Symptom: Failure to complete email login and multi-click mutual follow tasks due to React synthetic event drops and element interception
import asyncio
import logging

async def execute_email_login(page, email_selector: str, email_val: str, submit_selector: str):
    """Robust email form fill bypassing React/Vue synthetic event drops."""
    logging.info("Executing robust email login")
    await page.wait_for_selector(email_selector, state='visible', timeout=15000)
    input_el = page.locator(email_selector)
    await input_el.evaluate("el => el.value = ''")
    await input_el.type(email_val, delay=150)
    
    await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
    await page.locator(submit_selector).evaluate("el => el.click()")
    try:
        await page.wait_for_load_state('networkidle', timeout=10000)
    except Exception as e:
        logging.warning(f"Network idle timeout after submit, proceeding anyway: {e}")
    return True

async def execute_batch_follow(page, follow_btn_selector: str):
    """Iterates through follow buttons and clicks them via JS to bypass pointer-events blocking."""
    logging.info("Executing batch follow actions")
    await page.wait_for_selector(follow_btn_selector, state='attached', timeout=10000)
    buttons = await page.locator(follow_btn_selector).all()
    
    clicked = 0
    for btn in buttons:
        if await btn.is_visible():
            await btn.evaluate("el => el.click()")
            clicked += 1
            await page.wait_for_timeout(1500) # Prevent rate limits / shadow bans
            
    logging.info(f"Clicked {clicked} follow buttons")
    return clicked
