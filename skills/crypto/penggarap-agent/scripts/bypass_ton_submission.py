# Origin Domain: siloprotocol.xyz
# Date: 2026-08-20
# Symptom: Fails to complete tasks and submit TON address due to generic selector issues

import asyncio

async def bypass_task_and_submit(page, wallet_address: str, task_selector="a[href*='twitter.com'], a[href*='t.me'], button:has-text('Follow'), button:has-text('Join')", input_selector="input[placeholder*='TON' i], input[type='text']", submit_selector="button:has-text('Submit'), button:has-text('Claim')"):
    """
    Clicks available task links/buttons, fills TON wallet address, and submits.
    """
    # Click task links in background to satisfy completion requirements
    task_elements = await page.locator(task_selector).all()
    for el in task_elements:
        try:
            await el.click(modifiers=['Control'])
            await asyncio.sleep(1)
        except Exception:
            pass
            
    await page.bring_to_front()
    
    # Locate and fill the TON address input
    input_field = page.locator(input_selector).first
    if await input_field.is_visible(timeout=5000):
        await input_field.fill(wallet_address)
        
        # Locate and click the submit button
        submit_btn = page.locator(submit_selector).first
        if await submit_btn.is_visible(timeout=5000):
            await submit_btn.click()
            await asyncio.sleep(2)
    return True
