# Metadata: docs.google.com, 2026-08-26, Complex nested DOM form inputs failing standard targeting

async def fill_aria_form(page, form_data: dict):
    """
    Generic form filler relying on ARIA roles and visible text rather than fragile CSS classes.
    form_data: { "Question text": "Answer text" | ["Option 1", "Option 2"] }
    """
    for field_label, value in form_data.items():
        container = page.locator(f"xpath=//div[contains(@role, 'listitem') or contains(@class, 'form-group')][contains(., '{field_label}')]")
        if isinstance(value, list):
            for opt in value:
                await container.locator(f"xpath=.//div[@role='checkbox'][contains(@aria-label, '{opt}') or contains(., '{opt}')]").click()
        else:
            text_input = container.locator("input[type='text'], input:not([type]), textarea").first
            radio_opt = container.locator(f"xpath=.//div[@role='radio' or @role='option'][contains(@aria-label, '{value}') or contains(., '{value}')]").first
            if await text_input.count() > 0:
                await text_input.fill(str(value))
            elif await radio_opt.count() > 0:
                await radio_opt.click()
            else:
                await page.get_by_text(str(value)).first.click()
