# Origin Domain: docs.google.com
# Date: 2026-08-20
# Symptom: Automation fails on forms with obfuscated CSS classes; relies on ARIA labels and roles.

async def fill_aria_input(page, label_text: str, value: str):
    """Fill input relying on aria-label or visible text proximity."""
    el = page.locator(f'input[aria-label*="{label_text}"], textarea[aria-label*="{label_text}"]').first
    if await el.count() > 0:
        await el.fill(value)
        return
    el = page.locator(f'text="{label_text}"').locator('xpath=ancestor::div[1]//input | ancestor::div[1]//textarea').first
    await el.fill(value)

async def select_aria_radio(page, option_text: str):
    """Click radio/checkbox relying on aria-label or role."""
    el = page.locator(f'[role="radio"][aria-label*="{option_text}"], [role="checkbox"][aria-label*="{option_text}"]').first
    await el.click()

async def submit_aria_form(page, submit_text: str = "Submit"):
    """Click the submit button by role and text."""
    el = page.locator(f'[role="button"]:has-text("{submit_text}"), [role="button"]:has-text("Kirim")').first
    await el.click()
