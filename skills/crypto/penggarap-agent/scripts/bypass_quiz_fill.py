# Metadata: Origin Domain: rewards.svpstars.com, Date: 2026-09-26, Symptom: Daily quiz form dynamic input targeting

async def bypass_quiz_fill(page, answers: list, submit_btn: str = "button[type='submit'], button:has-text('Submit')"):
    for answer in answers:
        el = page.get_by_text(answer, exact=True)
        if await el.count() > 0:
            await el.first.click()
            continue
        
        empty_inputs = page.locator("input:not([type='hidden']):not([type='radio']):not([type='checkbox']), textarea")
        for i in range(await empty_inputs.count()):
            input_el = empty_inputs.nth(i)
            if not await input_el.input_value():
                await input_el.fill(answer)
                break
        await page.wait_for_timeout(500)
        
    if submit_btn:
        btn = page.locator(submit_btn)
        if await btn.count() > 0:
            await btn.first.click()