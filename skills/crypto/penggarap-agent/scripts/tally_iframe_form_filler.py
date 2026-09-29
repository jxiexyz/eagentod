# Metadata: Origin Domain: ax1.vc, Date: 2026-08-26, Symptom: Cannot interact with embedded Tally form (cross-origin iframe block)

from playwright.sync_api import Page, FrameLocator

def get_tally_frame(page: Page, iframe_selector: str = 'iframe[src*="tally.so"]') -> FrameLocator:
    """
    Resolves and returns the Playwright FrameLocator for an embedded Tally form.
    Waits for the iframe to attach and load.
    """
    page.wait_for_selector(iframe_selector, state='attached', timeout=15000)
    return page.frame_locator(iframe_selector)

def fill_tally_form(page: Page, field_selectors: dict, submit_text: str = 'Submit'):
    """
    Generic helper to fill a Tally form inside an iframe.
    field_selectors: dict mapping CSS selectors to their string values.
    """
    frame = get_tally_frame(page)
    
    for selector, value in field_selectors.items():
        input_loc = frame.locator(selector).first
        input_loc.wait_for(state='visible', timeout=10000)
        input_loc.fill(value)
        
    submit = frame.locator('button').filter(has_text=submit_text).first
    if submit:
        submit.wait_for(state='visible', timeout=5000)
        submit.click()
