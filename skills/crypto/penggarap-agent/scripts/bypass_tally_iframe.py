# Metadata: Domain: Generic (origin: app.c8ntinuum.com), Date: 2026-08-26, Symptom: Playwright cannot directly interact with embedded Tally.so iframe forms.

async def bypass_tally_iframe(page, form_data: dict, auto_submit: bool = True):
    """
    Fills out a Tally form embedded in a cross-origin iframe.
    page: Playwright async page object.
    form_data: dict mapping label/placeholder text to values.
    """
    frame = page.frame_locator('iframe[src*="tally.so"]').first
    
    for key, val in form_data.items():
        target = frame.get_by_placeholder(key, exact=False).or_(frame.get_by_label(key, exact=False))
        
        count = await target.count()
        if count == 0:
            target = frame.locator(f'div:has-text("{key}")').last.locator('input, textarea').first
            
        await target.fill(str(val))
        await page.wait_for_timeout(200)
        
    if auto_submit:
        btn = frame.locator('button:has-text("Submit"), button:has-text("Join"), button[type="submit"]').first
        await btn.click()
        await page.wait_for_timeout(3000)
        
    return True
