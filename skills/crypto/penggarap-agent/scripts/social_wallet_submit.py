# Metadata: Origin Domain: theinkylabs.xyz, Date: 2026-08-25, Symptom: Social task & EVM wallet submission blocker
import asyncio

async def bypass_social_and_submit_wallet(page, wallet_address: str, social_selectors: list, wallet_input_selector: str, submit_btn_selector: str):
    """
    Generic bypass for social task completion and wallet submission.
    """
    for selector in social_selectors:
        try:
            if await page.locator(selector).is_visible(timeout=3000):
                await page.click(selector)
                await asyncio.sleep(1.5)
        except Exception as e:
            print(f"Skipping {selector}: {e}")

    try:
        await page.wait_for_selector(wallet_input_selector, timeout=5000)
        await page.fill(wallet_input_selector, wallet_address)
        await asyncio.sleep(0.5)
        await page.click(submit_btn_selector)
        await asyncio.sleep(2)
    except Exception as e:
        print(f"Wallet submission failed: {e}")
        return False
    return True
