# Metadata: Origin Domain: docs.google.com, Date: 2026-08-25, Symptom: Playwright .fill() fails to trigger Material/React state updates

async def fill_material_input(page, selector: str, value: str):
    """Bypass for inputs requiring human-like interaction to trigger state."""
    element = await page.wait_for_selector(selector, state="visible", timeout=10000)
    await element.scroll_into_view_if_needed()
    await element.click()
    await page.keyboard.press("Control+a")
    await page.keyboard.press("Backspace")
    await page.keyboard.type(value, delay=50)
    await page.wait_for_timeout(200)

async def submit_material_form(page, submit_selector: str = "div[role='button']"):
    element = await page.wait_for_selector(submit_selector, state="visible")
    await element.scroll_into_view_if_needed()
    await element.click()
    await page.wait_for_load_state("networkidle")