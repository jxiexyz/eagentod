# Metadata: Origin Domain: hub.axisrobotics.ai | Date: 2026-08-27 | Symptom: Social tasks and wallet submission failing
import asyncio

async def run(page, wallet_address, start_selector="text=Start", wallet_input_selector="input[placeholder*='address' i], input[type='text']", submit_selector="text=Submit"):
    """
    Bypasses standard social task UI and wallet submission.
    """
    try:
        if await page.locator(start_selector).is_visible():
            await page.locator(start_selector).click()
            await asyncio.sleep(2)
        
        input_loc = page.locator(wallet_input_selector).first
        if await input_loc.is_visible():
            await input_loc.fill(wallet_address)
            await asyncio.sleep(1)
        
        submit_loc = page.locator(submit_selector).first
        if await submit_loc.is_visible():
            await submit_loc.click()
            await asyncio.sleep(2)
            
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
