# Metadata: Origin Domain: docs.google.com | Date: 2026-08-20 | Symptom: Fails to fill text inputs and select from ARIA listbox dropdowns.
import asyncio

async def bypass_form_fill(page, text_selector: str, text_value: str, listbox_selector: str, option_text: str):
    await page.locator(text_selector).first.fill(text_value)
    await page.locator(listbox_selector).first.click()
    await asyncio.sleep(0.5)
    await page.locator(f'[role="option"]:has-text("{option_text}")').first.click()
