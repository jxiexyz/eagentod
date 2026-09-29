# Origin Domain: ax1.vc
# Date: 2026-08-26
# Symptom: Tally form interactions fail because inputs are encapsulated in a cross-origin iframe and rely on React synthetic events.

from playwright.sync_api import Page

def fill_embedded_form(page: Page, iframe_selector: str, fields: dict, submit_btn_selector: str = None):
    """
    Safely interacts with inputs trapped inside a cross-origin iframe (e.g., Tally.so, Typeform).
    
    :param page: Playwright Page object.
    :param iframe_selector: CSS selector for the iframe element.
    :param fields: Dictionary mapping element selectors (inside the iframe) to their string values.
    :param submit_btn_selector: Optional CSS selector for the submit button.
    """
    frame_loc = page.frame_locator(iframe_selector).first
    
    for selector, value in fields.items():
        element = frame_loc.locator(selector).first
        element.wait_for(state="visible", timeout=10000)
        element.scroll_into_view_if_needed()
        # Sequential click then fill ensures React/Vue event listeners fire properly
        element.click()
        page.wait_for_timeout(300)
        element.fill(value)
        page.wait_for_timeout(300)
        
    if submit_btn_selector:
        submit_btn = frame_loc.locator(submit_btn_selector).first
        submit_btn.wait_for(state="visible", timeout=5000)
        submit_btn.scroll_into_view_if_needed()
        submit_btn.click()
        # Allow network request to fire post-submit
        page.wait_for_timeout(2000)
