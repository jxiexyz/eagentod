# Metadata: docs.google.com, 2026-08-23, Form element targeting failure (dynamic IDs)

from playwright.async_api import Page

async def bypass_form_by_labels(page: Page, fields: dict, submit_text: str = "Submit"):
    for label, value in fields.items():
        lbl = page.get_by_text(label, exact=False).first
        container = lbl.locator("xpath=ancestor::*[.//input or .//*[@role='radio'] or .//*[@role='checkbox']][1]")
        
        if await container.count() > 0:
            txt = container.locator('input:not([type="radio"]):not([type="checkbox"]), textarea').first
            if await txt.count() > 0 and await txt.is_visible():
                await txt.fill(str(value))
                continue
            
            opt = container.locator(f'*[role="radio"][data-value="{value}"], *[role="checkbox"][data-value="{value}"], label:has-text("{value}")').first
            if await opt.count() > 0 and await opt.is_visible():
                await opt.click()
                
    if submit_text:
        btn = page.locator(f'button:has-text("{submit_text}"), [role="button"]:has-text("{submit_text}")').first
        if await btn.count() > 0 and await btn.is_visible():
            await btn.click()
            await page.wait_for_load_state("networkidle")
