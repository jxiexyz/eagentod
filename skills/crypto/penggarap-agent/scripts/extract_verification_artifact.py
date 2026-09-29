# Metadata: Origin Domain: hedgelords.cash, Date: 2026-08-19, Symptom: Worker claims success but fails to capture/return a valid verification artifact.

def extract_verification_artifact(page, success_selectors=None, timeout_ms=10000):
    """
    Wait for and extract a verification artifact (text or element) to prove task success.
    """
    if success_selectors is None:
        success_selectors = [
            'text="Success"',
            'text="Congratulations"',
            'text="submitted"',
            'text="Whitelist"',
            '.success-message',
            '[data-testid="success"]',
            '.tx-hash'
        ]
        
    try:
        page.wait_for_load_state('networkidle', timeout=timeout_ms)
    except Exception:
        pass
        
    for selector in success_selectors:
        try:
            element = page.locator(selector).first
            if element.is_visible(timeout=2000):
                return {"status": "success", "artifact": element.inner_text()}
        except Exception:
            continue
            
    return {
        "status": "fallback", 
        "url": page.url, 
        "artifact": "No specific selector matched. Fallback to URL state."
    }