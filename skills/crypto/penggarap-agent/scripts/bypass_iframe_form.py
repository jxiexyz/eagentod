# Metadata: Origin: playground.rialo.io | Date: 2026-08-23 | Symptom: Unable to interact with embedded iframe forms (e.g., Tally) cross-origin context.
from playwright.sync_api import Page, Frame

def get_form_frame(page: Page, src_keyword: str = "tally.so", timeout: int = 15000) -> Frame:
    """Resolves cross-origin form iframes by src keyword."""
    selector = f'iframe[src*="{src_keyword}"]'
    page.wait_for_selector(selector, state='attached', timeout=timeout)
    for frame in page.frames:
        if src_keyword in frame.url:
            frame.wait_for_selector('form', state='attached', timeout=timeout)
            return frame
    return None

def submit_iframe_form(page: Page, src_keyword: str, field_mapping: dict, submit_text: str = "Submit") -> bool:
    """
    Fills and submits a form inside an iframe.
    field_mapping: dict of {placeholder_or_label: value}
    ponytail: basic text inputs handled. complex dropdowns need separate logic.
    """
    frame = get_form_frame(page, src_keyword)
    if not frame:
        return False
        
    for key, val in field_mapping.items():
        input_el = frame.get_by_placeholder(key)
        if input_el.count() == 0:
            input_el = frame.get_by_text(key).locator("xpath=following::input[1]")
        if input_el.count() > 0:
            input_el.first.fill(val)
            
    btn = frame.get_by_role("button", name=submit_text)
    if btn.count() > 0:
        btn.first.click()
        page.wait_for_timeout(2000)
        return True
    return False
