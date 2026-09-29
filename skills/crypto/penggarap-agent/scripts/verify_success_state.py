# Origin Domain: zygofuture.com
# Date: 2026-08-17
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

async def verify_success_state(page, target_selectors=None, timeout=10000):
    """
    Scans for verification artifacts (success messages, transaction hashes).
    """
    if target_selectors is None:
        target_selectors = [
            "[class*='success']",
            "text='Success'",
            "text='Claimed'",
            "text='Congratulations'",
            ".modal:visible",
            "[role='alert']"
        ]
        
    for selector in target_selectors:
        try:
            element = await page.wait_for_selector(selector, timeout=timeout/len(target_selectors), state="visible")
            if element:
                text = await element.inner_text()
                if text.strip():
                    return {"verified": True, "artifact": text.strip(), "selector": selector}
        except:
            continue
            
    return {
        "verified": False, 
        "url": page.url,
        "error": "No success indicator found within timeout."
    }