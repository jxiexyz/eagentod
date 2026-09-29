# Metadata: Origin Domain: rewards.canopynetwork.org, Date: 2026-08-26, Symptom: Social follow and wallet submit automation blocked/timeout
import asyncio
from playwright.async_api import Page

async def bypass_social_submit(page: Page, wallet_address: str, social_selectors: list = None, wallet_selector: str = "input[placeholder*='BSC' i], input[placeholder*='address' i], input[type='text']", submit_selector: str = "button:has-text('Submit'), button:has-text('Confirm')"):
    if social_selectors:
        for selector in social_selectors:
            try:
                await page.click(selector, timeout=3000)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"Skip {selector}: {e}")
    try:
        input_element = await page.wait_for_selector(wallet_selector, state="visible", timeout=5000)
        await input_element.fill(wallet_address)
        await asyncio.sleep(1)
        submit_btn = await page.wait_for_selector(submit_selector, state="visible", timeout=3000)
        await submit_btn.click()
    except Exception as e:
        print(f"Submit error: {e}")
    return True
