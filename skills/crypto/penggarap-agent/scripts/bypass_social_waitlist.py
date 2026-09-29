# Metadata:
# Origin Domain: app.zen-o.xyz
# Date: 2026-08-23
# Specific Symptom: Fails to complete social tasks and submit EVM address due to window focus loss or unhandled new tabs.

import asyncio
from playwright.async_api import Page

async def complete_waitlist_tasks(page: Page, task_selectors: list[str], input_selector: str, address: str, submit_selector: str):
    """
    Bypass social task verification by clicking and instantly closing resulting tabs, 
    then fill and submit the EVM address.
    """
    for selector in task_selectors:
        try:
            # Intercept and close new tabs (Twitter/Discord OAuth or intents) to maintain main page focus
            async with page.context.expect_page(timeout=3000) as new_page_info:
                await page.locator(selector).click(force=True)
            new_page = await new_page_info.value
            await new_page.close()
        except Exception:
            # If no new page spawned, just yield to allow UI state updates
            await asyncio.sleep(1)
            
    # Target input, allowing for shadow DOM penetration via standard locator
    input_loc = page.locator(input_selector)
    await input_loc.wait_for(state="visible", timeout=5000)
    await input_loc.fill(address, force=True)
    
    # Target submit
    await page.locator(submit_selector).click(force=True)
    
    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass
