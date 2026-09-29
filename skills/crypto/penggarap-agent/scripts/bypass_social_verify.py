# Origin Domain: theinkylabs.xyz
# Date: 2026-08-26
# Specific Symptom: Fails to complete social channel join and verification flow due to new tab popups preventing main page context progression.

import asyncio
import logging

async def bypass_social_verify(page, action_selector: str, verify_selector: str = None, wait_time: int = 3):
    """
    Generic bypass for social tasks (Join TG/Discord/Twitter -> Verify).
    Clicks the action link, intercepts/closes the resulting popup/new tab,
    waits, and clicks verify.
    """
    logging.info(f"Executing social bypass on {action_selector}")
    
    try:
        # Watch for new pages (popups) while clicking
        async with page.context.expect_page(timeout=5000) as new_page_info:
            await page.click(action_selector)
        
        new_page = await new_page_info.value
        await new_page.close()
        logging.info("Closed popup/new tab automatically.")
    except Exception as e:
        # Fallback if no page actually opened or it opened in same tab
        logging.warning(f"No new page intercepted or click failed: {e}")
        try:
            await page.click(action_selector, force=True)
        except Exception:
            pass
        
    await asyncio.sleep(wait_time)
    
    if verify_selector:
        logging.info(f"Clicking verify: {verify_selector}")
        await page.click(verify_selector, force=True)
        await asyncio.sleep(2)
        
    return True
