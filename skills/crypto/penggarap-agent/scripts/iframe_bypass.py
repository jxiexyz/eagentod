# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-23, Symptom: Iframe DOM isolation blocking form access

async def get_iframe_context(page, iframe_selector='iframe'):
    frame = page.frame_locator(iframe_selector)
    await frame.locator('body').wait_for(state='attached')
    return frame
