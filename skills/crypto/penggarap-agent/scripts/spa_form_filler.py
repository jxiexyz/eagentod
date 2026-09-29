# Metadata: docs.google.com, 2026-08-25, Google Forms ARIA inputs rejecting standard locator.fill()

async def fill_spa_form(page, field_label: str, value: str, is_choice: bool = False):
    """Fallback filler for complex SPA forms using keyboard navigation."""
    if is_choice:
        await page.locator(f'text="{value}"').first.click()
    else:
        await page.locator(f'text="{field_label}"').first.click()
        await page.keyboard.press('Tab')
        await page.keyboard.type(value, delay=50)
