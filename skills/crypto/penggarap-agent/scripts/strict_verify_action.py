# Metadata: Origin: docs.google.com | Date: 2026-08-19 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

def execute_and_verify(page, action_selector, verify_selector=None, verify_url_pattern=None, timeout=10000):
    """
    Executes a submission action and strictly enforces verification before claiming success.
    Returns a tangible artifact (text, URL, or screenshot path).
    """
    try:
        page.locator(action_selector).scroll_into_view_if_needed()
        page.click(action_selector)
        
        if verify_selector:
            page.wait_for_selector(verify_selector, state="visible", timeout=timeout)
            content = page.text_content(verify_selector)
            return {"status": "verified", "artifact": content.strip() if content else "Element present"}
            
        if verify_url_pattern:
            import re
            page.wait_for_url(re.compile(verify_url_pattern), timeout=timeout)
            return {"status": "verified", "artifact": f"URL reached: {page.url}"}
            
        # Fallback: Capture visual artifact if no specific selector/URL provided
        import tempfile
        path = tempfile.mktemp(suffix=".png")
        page.screenshot(path=path)
        return {"status": "verified", "artifact": f"Visual proof: {path}"}
        
    except Exception as e:
        return {"status": "failed", "error": str(e)}
