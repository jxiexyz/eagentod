# Origin Domain: bridge.svpstars.com
# Date: 2026-09-27
# Specific Symptom: Quiz form submission failures / dynamic locators

async def fill_quiz(page, answers: list, submit_selector: str = "button[type='submit'], button:has-text('Submit')"):
    """
    ponytail: blind text match and empty-input fill. add label mapping if fields misalign.
    """
    for ans in answers:
        choice = page.locator(f"text='{ans}'")
        if await choice.count() > 0:
            await choice.first.click(force=True)
            continue
        
        inputs = page.locator("input:not([type='hidden']):not([type='radio']):not([type='checkbox']), textarea")
        for i in range(await inputs.count()):
            el = inputs.nth(i)
            if not await el.input_value():
                await el.fill(str(ans))
                break
                
    btn = page.locator(submit_selector)
    if await btn.count() > 0:
        await btn.first.click(force=True)
