# Metadata: Domain: rewards.svpstars.com, Date: 2026-09-27, Symptom: Daily quiz submission automation failure
import asyncio

async def bypass(page, answers, submit_selector="button[type='submit'], button:has-text('Submit')"):
    """
    Fills generic quizzes/forms. 
    Matches visible labels/radios by text, or fills the next empty text/url input.
    """
    for answer in answers:
        # 1. Try exact text match for radio/checkbox options
        label = page.locator(f"label:has-text('{answer}'), div[role='radio']:has-text('{answer}')").first
        if await label.is_visible():
            await label.click()
            await page.wait_for_timeout(500)
            continue
            
        # 2. Otherwise fill the next empty text input
        inputs = page.locator("input[type='text'], input[type='url'], textarea")
        for i in range(await inputs.count()):
            loc = inputs.nth(i)
            val = await loc.input_value()
            if not val:
                await loc.fill(answer)
                await page.wait_for_timeout(500)
                break
                
    # Submit form
    submit = page.locator(submit_selector).first
    if await submit.is_visible():
        await submit.click()
        await page.wait_for_timeout(2000)
