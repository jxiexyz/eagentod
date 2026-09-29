# Origin Domain: docs.google.com
# Date: 2026-08-25
# Specific Symptom: page.fill fails due to custom ARIA roles and obscured inputs.

async def bypass_google_form_field(page, question: str, value: str, field_type: str = "text"):
    container = page.locator(f'div[role="listitem"]:has-text("{question}")').first
    
    if field_type == "text":
        target = container.locator('input[type="text"], input[type="email"], textarea, input:not([type="hidden"])').first
        await target.fill(value)
    elif field_type in ["radio", "checkbox"]:
        target = container.locator(f'div[role="{field_type}"][data-value="{value}"], div[role="{field_type}"][aria-label="{value}"]')
        if await target.count() == 0:
            target = container.locator(f'label:has-text("{value}")')
        await target.first.click()
