# Metadata: Origin: rewards.svpstars.com, Date: 2026-09-19, Symptom: Automation fails on custom quiz forms requiring dynamic text matching
import asyncio

async def solve_quiz(page, answers, submit_selector="button:has-text('Submit'), button[type='submit']"):
    # ponytail: assumes multiple choice clickable answers. add input field filling when text boxes encountered.
    for answer in answers:
        try:
            loc = page.get_by_text(answer, exact=False).first
            await loc.wait_for(state="visible", timeout=3000)
            await loc.click()
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Skip answer '{answer}': {e}")
    
    try:
        btn = page.locator(submit_selector).first
        if await btn.count() > 0:
            await btn.click(timeout=3000)
    except Exception:
        pass
    return True