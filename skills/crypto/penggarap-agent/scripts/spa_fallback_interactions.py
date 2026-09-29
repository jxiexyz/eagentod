# Metadata: docs.google.com, 2026-08-20, Element click intercepted or fill fails on non-standard inputs

async def force_click(page, selector: str):
    element = await page.wait_for_selector(selector, state="attached")
    await element.scroll_into_view_if_needed()
    await page.evaluate("(el) => el.click()", element)

async def force_type(page, selector: str, text: str):
    await page.wait_for_selector(selector, state="visible")
    await page.click(selector, force=True)
    await page.keyboard.down("Control")
    await page.keyboard.press("A")
    await page.keyboard.up("Control")
    await page.keyboard.press("Backspace")
    await page.keyboard.type(text, delay=30)
