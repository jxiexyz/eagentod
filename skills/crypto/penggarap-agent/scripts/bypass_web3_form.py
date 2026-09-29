# Metadata: thefallennft.com, 2026-08-27, Overlay blocking BSC address input or social task clicks

import asyncio
from playwright.async_api import Page

async def bypass_fill_input(page: Page, selector: str, value: str):
    try:
        element = page.locator(selector).first
        await element.wait_for(state="visible", timeout=15000)
        await element.scroll_into_view_if_needed()
        await element.click(force=True)
        await element.fill("")
        await page.keyboard.type(value, delay=50)
        return True
    except Exception as e:
        print(f"[bypass_web3_form] Failed: {e}")
        return False
