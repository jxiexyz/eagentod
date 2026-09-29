# Metadata: Origin Domain: feralhood.xyz, Date: 2026-08-21, Symptom: Embedded Google Form unresolvable or inputs unfillable due to iframe context.
import asyncio

async def resolve_and_fill_gform(page, fields: dict):
    """
    Finds Google Form iframe (if embedded) and fills fields by label.
    fields: dict of { "Exact Label Text": "Value to Fill" }
    """
    frame = page
    for f in page.frames:
        if "docs.google.com/forms" in f.url:
            frame = f
            break

    for label, value in fields.items():
        container = frame.locator(f"xpath=//div[@role='listitem'][.//span[normalize-space(text())='{label}']]")
        input_el = container.locator("input[type='text'], input[type='email'], textarea").first
        await input_el.scroll_into_view_if_needed()
        await input_el.fill(value)
        await asyncio.sleep(0.2)

    submit_btn = frame.locator("div[role='button']:has-text('Submit'), div[role='button']:has-text('Kirim')").first
    if await submit_btn.count() > 0:
        await submit_btn.click()
        await page.wait_for_timeout(2000)
    return True
