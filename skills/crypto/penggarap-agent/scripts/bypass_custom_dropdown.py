# Metadata: Origin Domain: nft.retium.org, Date: 2026-08-20, Symptom: Form submission fails because country selector is a custom UI element, not a native <select>.

def bypass_custom_dropdown(page, dropdown_trigger_selector: str, option_text: str):
    """
    Bypasses standard select_option failures by clicking the trigger and explicitly locating the text option.
    """
    trigger = page.locator(dropdown_trigger_selector).first
    trigger.wait_for(state='visible', timeout=5000)
    trigger.click()
    
    page.wait_for_timeout(1000)
    
    option = page.get_by_text(option_text, exact=True).first
    if not option.is_visible():
        option = page.get_by_text(option_text).first
        
    option.wait_for(state='visible', timeout=5000)
    option.click()
    page.wait_for_timeout(500)
    return True