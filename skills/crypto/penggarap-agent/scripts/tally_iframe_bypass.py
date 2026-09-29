# Origin Domain: ax1.vc
# Date: 2026-08-26
# Symptom: Cannot interact with Tally form due to cross-origin iframe isolation.

async def fill_tally_iframe(page, data: dict, selector: str = "iframe[src*='tally.so']"):
    frame = page.frame_locator(selector).first
    await frame.locator("form").wait_for(state="visible")
    
    for label, val in data.items():
        field = frame.get_by_label(label, exact=False)
        if await field.count() == 0:
            field = frame.get_by_text(label, exact=False).locator("..//..//input | ..//..//textarea").first
        await field.fill(str(val))
        
    submit = frame.locator("button[type='submit'], button:has-text('Submit')").first
    await submit.click()
