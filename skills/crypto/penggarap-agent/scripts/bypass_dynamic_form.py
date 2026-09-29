# Metadata: Origin Domain: Generic (tally.so), Date: 2026-08-26, Symptom: SPA dynamic form lazy load timeout blocking standard interaction

async def bypass_fill_form(page, fields: dict, submit_text: str = 'Submit'):
    try:
        await page.wait_for_load_state('networkidle', timeout=5000)
    except Exception:
        pass
    for label, val in fields.items():
        loc = page.get_by_label(label).first
        if not await loc.count():
            loc = page.get_by_placeholder(label).first
        if not await loc.count():
            loc = page.locator(f"xpath=//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]/following::input[1]").first
        await loc.scroll_into_view_if_needed()
        await loc.fill(str(val))
        await page.wait_for_timeout(250)
    if submit_text:
        btn = page.locator(f"button:has-text('{submit_text}'), button[type='submit']").first
        if await btn.count():
            await btn.scroll_into_view_if_needed()
            await btn.click()
            await page.wait_for_load_state('networkidle', timeout=5000)
