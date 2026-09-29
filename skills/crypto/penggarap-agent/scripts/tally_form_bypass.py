# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-23, Symptom: Iframe isolation blocking standard DOM access on Tally forms

async def fill_tally_form(page, form_data, iframe_selector="iframe[src*='tally.so']", submit_selector=None):
    """
    Fills elements inside a cross-origin Tally form iframe.
    form_data: dict of {selector: value}. Use '[CLICK]' for buttons.
    """
    iframe_element = await page.wait_for_selector(iframe_selector, state='attached', timeout=15000)
    frame = await iframe_element.content_frame()
    if not frame:
        raise Exception('Tally iframe not found or inaccessible')
    
    for selector, value in form_data.items():
        el = await frame.wait_for_selector(selector, state='visible', timeout=10000)
        if isinstance(value, bool):
            await el.check() if value else await el.uncheck()
        elif value == '[CLICK]':
            await el.click()
        else:
            await el.fill(str(value))
            
    if submit_selector:
        btn = await frame.wait_for_selector(submit_selector, state='visible', timeout=5000)
        await btn.click()
        
    return True
