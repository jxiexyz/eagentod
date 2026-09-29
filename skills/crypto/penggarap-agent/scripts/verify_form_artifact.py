# Metadata: Origin: docs.google.com | Date: 2026-08-19 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

import time

def extract_submission_artifact(page, success_selectors=None, fallback_text="response has been recorded"):
    """
    Generic verification artifact extractor for web forms.
    Extracts confirmation text and screenshot to satisfy the Worker's artifact requirement.
    """
    if success_selectors is None:
        # Default Google Forms selectors and generic fallbacks
        success_selectors = [
            ".vHW8K", 
            ".freebirdFormviewerViewResponseConfirmationMessage",
            "div[role='heading'] + div",
            "text=recorded",
            "text=received",
            "text=submitted"
        ]
        
    try:
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception:
        pass # Proceed even if network doesn't completely idle
    
    artifact_data = {"verified": False, "text": "", "screenshot": None}
    
    for selector in success_selectors:
        try:
            locator = page.locator(selector).first
            if locator.is_visible(timeout=2000):
                artifact_data["text"] = locator.inner_text()
                artifact_data["verified"] = True
                break
        except Exception:
            continue
            
    # Fallback to scanning body text
    if not artifact_data["verified"]:
        try:
            body_text = page.locator("body").inner_text(timeout=2000)
            if fallback_text.lower() in body_text.lower():
                artifact_data["text"] = fallback_text
                artifact_data["verified"] = True
        except Exception:
            pass
            
    if artifact_data["verified"]:
        filename = f"/tmp/form_submit_{int(time.time())}.png"
        try:
            page.screenshot(path=filename)
            artifact_data["screenshot"] = filename
        except Exception:
            pass
            
    return artifact_data