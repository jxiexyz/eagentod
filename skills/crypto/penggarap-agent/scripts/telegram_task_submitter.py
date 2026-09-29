# Metadata: Origin Domain: jacon.codes, Date: 2026-08-27, Symptom: Failure to execute Telegram bot start and BSC address submission

from playwright.async_api import Page

async def execute_bot_and_submit_address(
    page: Page, 
    start_selector: str = 'button:has-text("Start"), text="Start"',
    address_input_selector: str = 'input[placeholder*="address" i], input[placeholder*="BSC" i]',
    submit_selector: str = 'button:has-text("Submit"), button:has-text("Confirm")',
    wallet_address: str = ""
):
    """
    Generic bypass to click a start button, fill a wallet address, and submit.
    """
    try:
        start_el = page.locator(start_selector).first
        if await start_el.is_visible(timeout=5000):
            await start_el.click()
            await page.wait_for_timeout(2000)
    except Exception as e:
        print(f"Start button bypass skipped: {e}")

    if wallet_address:
        try:
            input_el = page.locator(address_input_selector).first
            if await input_el.is_visible(timeout=5000):
                await input_el.fill(wallet_address)
                
                submit_el = page.locator(submit_selector).first
                if await submit_el.is_visible(timeout=3000):
                    await submit_el.click()
        except Exception as e:
            print(f"Address submission bypass skipped: {e}")
