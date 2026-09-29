# Origin Domain: forms.gle (Generic Web Forms)
# Date: 2026-08-22
# Symptom: Failure to find and fill dynamically generated form fields relying on divs and complex ARIA structures rather than standard HTML inputs.

import asyncio

async def fill_dynamic_form(page, field_data: dict, submit_text: str = "Submit"):
    """
    Fills heavily nested or dynamic forms (like Google Forms) using XPath proximity.
    field_data: dict mapping label substring to value.
    """
    for label, value in field_data.items():
        # Target complex div-based structures or standard labels
        target = page.locator(f"//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]/ancestor::div[not(position()>3)]//input | //span[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]/ancestor::div[not(position()>5)]//input").first
        
        if not await target.is_visible():
            # Fallback to textarea
            target = page.locator(f"//div[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]/ancestor::div[not(position()>3)]//textarea").first

        if await target.is_visible():
            await target.click()
            await page.keyboard.type(value, delay=50)
            await page.wait_for_timeout(300)

    if submit_text:
        submit_btn = page.locator(f"//div[@role='button'][contains(., '{submit_text}')] | //button[contains(., '{submit_text}')]").first
        if await submit_btn.is_visible():
            await submit_btn.click()
            await page.wait_for_timeout(2000)
