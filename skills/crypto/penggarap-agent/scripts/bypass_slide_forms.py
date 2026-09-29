# Metadata: Origin Domain: typeform.com, Date: 2026-08-23, Symptom: Slide-based forms failing due to UI animations and custom next buttons.

import asyncio
from playwright.async_api import Page, expect

async def fill_slide_and_advance(page: Page, input_selector: str, value: str, advance_key: str = 'Enter', next_btn_selector: str = 'button[data-qa="ok-button"]'):
    """
    Handles animated slide forms by waiting for visibility, filling, and advancing via Enter or Next button.
    """
    input_loc = page.locator(input_selector).first
    await expect(input_loc).to_be_visible(timeout=10000)
    await input_loc.click()
    await page.wait_for_timeout(300)
    await input_loc.fill(value)
    await page.wait_for_timeout(500)
    
    next_btn = page.locator(next_btn_selector).first
    if await next_btn.is_visible():
        await next_btn.click()
    else:
        await input_loc.press(advance_key)
        
    await page.wait_for_timeout(1500)
