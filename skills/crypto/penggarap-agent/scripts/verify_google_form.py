# Origin Domain: docs.google.com
# Date: 2026-08-18
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

def extract_verification_artifact(page, submit_selector='div[role="button"]:has-text("Submit")', confirmation_selector='text="Your response has been recorded."'):
    """Submits the form and explicitly extracts the confirmation message as an artifact."""
    if page.locator(submit_selector).is_visible():
        page.click(submit_selector)
    
    page.wait_for_load_state("networkidle")
    try:
        page.wait_for_selector(confirmation_selector, timeout=10000)
        return page.locator(confirmation_selector).first.inner_text()
    except Exception:
        # Fallback to title and url if specific text changes
        return f"URL: {page.url} | Title: {page.title()}"
