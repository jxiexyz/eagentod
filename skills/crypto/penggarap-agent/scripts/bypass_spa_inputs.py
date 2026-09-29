# Origin Domain: inkersnft.xyz (Generic SPA)
# Date: 2026-08-25
# Specific Symptom: React/SPA inputs not binding state via standard page.fill(), causing validation failures on submission.

async def bypass_spa_form(page, fields_dict, submit_selector=None):
    """
    Fills SPA forms by forcing native keystrokes to trigger React/Vue synthetic events.
    fields_dict: dict of { 'selector': 'value' }
    """
    for selector, value in fields_dict.items():
        loc = page.locator(selector).first
        await loc.wait_for(state='attached', timeout=5000)
        await loc.scroll_into_view_if_needed()
        await loc.click()
        await page.keyboard.press('Control+A')
        await page.keyboard.press('Backspace')
        await loc.press_sequentially(value, delay=50)
    
    if submit_selector:
        btn = page.locator(submit_selector).first
        await btn.scroll_into_view_if_needed()
        try:
            await btn.click(timeout=3000)
        except Exception:
            # Fallback to direct DOM execution if intercepted/overlapped
            await page.evaluate('(sel) => document.querySelector(sel).click()', submit_selector)