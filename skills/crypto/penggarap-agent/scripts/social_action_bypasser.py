# Metadata: Origin Domain: spinelab.fun, Date: 2026-08-25, Symptom: Social link popups blocking flow and strict JS form validation on BSC address inputs.
import asyncio
from playwright.async_api import Page

async def handle_social_and_submit(page: Page, action_selector: str = None, verify_selector: str = None, input_selector: str = None, input_text: str = None):
    if action_selector:
        try:
            async with page.context.expect_page(timeout=4000) as new_page_info:
                await page.locator(action_selector).click(timeout=4000)
                new_page = await new_page_info.value
                await new_page.close()
        except Exception:
            pass
        await asyncio.sleep(2)

    if verify_selector:
        try:
            await page.locator(verify_selector).click(timeout=4000)
            await asyncio.sleep(2)
        except Exception:
            pass

    if input_selector and input_text:
        field = page.locator(input_selector)
        await field.wait_for(state="visible", timeout=5000)
        await field.click()
        await field.fill("")
        await field.type(input_text, delay=150)
        await page.keyboard.press("Tab")
