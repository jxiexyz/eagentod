# Metadata: Origin Domain: sweepwidget.com, Date: 2026-08-17, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

async def extract_verification_artifact(page, selectors=None, timeout=5000):
    """
    Extracts the user's current entry count or success state to serve as a verifiable artifact.
    """
    if not selectors:
        selectors = [
            ".sw_user_entries_amount",
            ".sw_entries_count",
            ".entry-count",
            ".user-entries",
            "[data-test='entries-count']"
        ]
        
    for sel in selectors:
        try:
            el = await page.wait_for_selector(sel, timeout=timeout, state='visible')
            if el:
                val = await el.inner_text()
                if val and val.strip():
                    return f"Artifact [{sel}]: {val.strip()}"
        except:
            pass
            
    # Generic fallback text scan
    try:
        body_text = await page.evaluate("document.body.innerText")
        for keyword in ["You've entered", "Entries:", "Thanks for entering"]:
            if keyword in body_text:
                return f"Artifact [Body Text]: {keyword}"
    except:
        pass
        
    raise Exception("Verification artifact not found - actions likely failed to register.")