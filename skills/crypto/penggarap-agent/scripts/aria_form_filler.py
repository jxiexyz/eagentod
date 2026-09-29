# Metadata: Origin Domain: docs.google.com, Date: 2026-08-24, Symptom: Failure to locate and fill dynamic form elements due to obfuscated CSS classes.
import asyncio

async def fill_form_by_aria(page, form_data: dict):
    """
    Generic form filler using ARIA roles and labels to bypass obfuscated CSS classes.
    form_data: dict mapping accessible name (or partial text) to value/action.
    """
    for label, value in form_data.items():
        # Try finding an input/textarea by its associated aria-label
        input_locator = page.locator(f"input[aria-label*='{label}' i], textarea[aria-label*='{label}' i]").first
        if await input_locator.is_visible():
            await input_locator.fill(str(value))
            continue
            
        # Try finding radio/checkbox by label value
        radio_locator = page.locator(f"div[role='radio'][aria-label*='{value}' i], div[role='checkbox'][aria-label*='{value}' i]").first
        if await radio_locator.is_visible():
            await radio_locator.click()
            continue
            
        # Fallback to exact text matching for clicks
        text_locator = page.get_by_text(str(value), exact=True).first
        if await text_locator.is_visible():
            await text_locator.click()
            
    # Attempt to click standard submit buttons
    submit_btn = page.locator("div[role='button'][aria-label*='Submit' i], div[role='button'][aria-label*='Kirim' i], button[type='submit']").first
    if await submit_btn.is_visible():
        await submit_btn.click()
    
    await page.wait_for_load_state('networkidle')
    return True
