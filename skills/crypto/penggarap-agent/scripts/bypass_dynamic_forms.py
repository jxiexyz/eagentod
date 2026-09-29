# Metadata: docs.google.com, 2026-08-26, Dynamic ID / Form submission failure
import asyncio
from playwright.async_api import Page

async def bypass_dynamic_form(page: Page, field_mapping: dict):
    """
    Bypass for dynamic forms (like Google Forms) that use obfuscated classes/IDs.
    field_mapping: dict of { "label_or_aria": "value_to_fill" }
    """
    for label, value in field_mapping.items():
        input_locator = page.locator(f'input[aria-label*="{label}" i], textarea[aria-label*="{label}" i]')
        if await input_locator.count() > 0:
            await input_locator.first.fill(value)
            continue
        
        radio_locator = page.locator(f'div[role="radio"][aria-label*="{value}" i], div[data-value="{value}"]')
        if await radio_locator.count() > 0:
            await radio_locator.first.click()
            continue

    submit_buttons = page.locator('div[role="button"]:has-text("Submit"), div[role="button"]:has-text("Next")')
    if await submit_buttons.count() > 0:
        await submit_buttons.last.click()
        await page.wait_for_load_state("networkidle")
