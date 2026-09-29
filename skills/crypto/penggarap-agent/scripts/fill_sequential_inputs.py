# Metadata: rewards.svpstars.com, 2026-09-27, Sequential Quiz Form Submission
import asyncio

async def bypass(page, answers: list, submit_selector: str = "button[type='submit'], button:has-text('Submit')"):
    elements = await page.locator("input:not([type='hidden']):not([type='radio']):not([type='checkbox']), textarea").all()
    for i, answer in enumerate(answers):
        if i < len(elements):
            await elements[i].fill(str(answer))
            await asyncio.sleep(0.3)
    if submit_selector:
        submit_btn = page.locator(submit_selector).first
        if await submit_btn.is_visible():
            await submit_btn.click()
            await asyncio.sleep(2)
