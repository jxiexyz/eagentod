# Metadata: docs.google.com, 2026-08-20, Element interception or timeout on obfuscated form elements (Google Forms)

async def force_click_aria(page, label, role='button'):
    """Force clicks an element identified by ARIA role and label, bypassing overlay interceptions."""
    locator = page.locator(f'[role="{role}"][aria-label*="{label}"], [role="{role}"]:has-text("{label}")').first
    await locator.scroll_into_view_if_needed()
    await locator.evaluate('(element) => element.click()')

async def fill_aria_textbox(page, label, text):
    """Fills an ARIA textbox by label."""
    locator = page.locator(f'input[aria-label*="{label}"], textarea[aria-label*="{label}"], [role="textbox"][aria-label*="{label}"]').first
    await locator.scroll_into_view_if_needed()
    await locator.fill(text)
