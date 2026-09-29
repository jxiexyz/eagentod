# Origin Domain: tally.so
# Date: 2026-08-24
# Symptom: Form elements inaccessible due to iframe embedding or custom DOM wrappers.

async def bypass(page, **kwargs):
    await page.wait_for_load_state('domcontentloaded')
    
    iframe = await page.query_selector('iframe[src*="tally.so"]')
    frame = await iframe.content_frame() if iframe else page.main_frame
    
    await frame.wait_for_selector('input, textarea, [role="button"], [role="checkbox"], [role="radio"]', state='attached', timeout=15000)
    
    return frame
