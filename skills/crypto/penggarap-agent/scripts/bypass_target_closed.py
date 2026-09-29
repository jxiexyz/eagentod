# Metadata: takeapeak.ai, 2026-08-20, Target page, context or browser has been closed during goto
import asyncio
from playwright.async_api import Error

async def bypass_target_closed(page, url, timeout=45000):
    """
    Bypass for 'Target page, context or browser has been closed' on page.goto.
    Tries to navigate; if the target closes, recovers by creating a new page in the same context.
    Returns the active page object.
    """
    try:
        await page.goto(url, timeout=timeout, wait_until="domcontentloaded")
        return page
    except Error as e:
        error_msg = str(e)
        if "Target page, context or browser has been closed" in error_msg or "Target closed" in error_msg:
            print(f"Detected target closed error: {error_msg}. Recovering...")
            try:
                context = page.context
                new_page = await context.new_page()
                await new_page.goto(url, timeout=timeout, wait_until="commit")
                return new_page
            except Exception as recovery_error:
                print(f"Recovery failed: {recovery_error}")
                raise recovery_error
        else:
            raise e
