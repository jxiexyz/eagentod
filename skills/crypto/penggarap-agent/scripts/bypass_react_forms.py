# Origin Domain: tally.so
# Date: 2026-08-24
# Symptom: Playwright .fill() fails to register input in React/Next.js state, or custom UI elements block standard clicks.

async def fill_react_input(page, selector: str, value: str):
    """
    Types into an input mimicking human behavior to trigger React synthetic events.
    """
    loc = page.locator(selector).first
    await loc.wait_for(state="visible", timeout=5000)
    await loc.click()
    await page.keyboard.down("Control")
    await page.keyboard.press("A")
    await page.keyboard.up("Control")
    await page.keyboard.press("Backspace")
    await loc.type(value, delay=30)
    await page.keyboard.press("Tab")

async def force_click_element(page, selector: str):
    """
    Forces a click on overlapping or custom div-based UI elements.
    """
    loc = page.locator(selector).first
    await loc.wait_for(state="attached", timeout=5000)
    await loc.scroll_into_view_if_needed()
    await loc.click(force=True)
