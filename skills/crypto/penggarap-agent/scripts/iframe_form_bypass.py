# Metadata: Origin Domain: app.c8ntinuum.com, Date: 2026-08-26, Symptom: Cross-origin iframe isolation blocking interaction with embedded Tally forms.

from playwright.sync_api import Page, FrameLocator

def resolve_form_iframe(page: Page, iframe_selector: str = 'iframe[src*="tally.so"]') -> FrameLocator:
    """
    Locates a cross-origin form iframe and waits for its internal form element to attach.
    """
    frame = page.frame_locator(iframe_selector)
    frame.locator('form').first.wait_for(state='attached', timeout=15000)
    return frame
