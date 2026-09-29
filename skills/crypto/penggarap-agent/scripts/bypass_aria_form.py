# Metadata: docs.google.com, 2026-08-22, Automation fails to locate and fill form fields (like BSC address) due to dynamic/obfuscated CSS classes.

async def fill_aria_form(page, form_data: dict, submit_text: str = "Submit"):
    """
    Generic ARIA-based form filler to bypass obfuscated classes.
    form_data: dict mapping question text (or substring) to the answer text.
    """
    for question, answer in form_data.items():
        # Locate generic list item containers wrapping the question
        q_container = page.locator(f'div[role="listitem"]:has-text("{question}")')
        
        # Handle text inputs
        text_box = q_container.locator('input[type="text"], textarea').first
        if await text_box.count() > 0:
            await text_box.fill(answer)
            continue
            
        # Handle radio/checkboxes
        choice = q_container.locator(f'[role="radio"]:has-text("{answer}"), [role="checkbox"]:has-text("{answer}")').first
        if await choice.count() > 0:
            await choice.click()
            continue
            
    # Submit the form
    submit_btn = page.locator(f'[role="button"]:has-text("{submit_text}")').first
    if await submit_btn.count() > 0:
        await submit_btn.click()
        
    await page.wait_for_load_state('networkidle')
    return True
