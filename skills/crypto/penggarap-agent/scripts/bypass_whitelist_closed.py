# Metadata: noirbrokers.fun, 2026-08-21, Whitelist closed / Campaign ended message blocks execution

def bypass(page, selectors=None, text_patterns=None):
    """
    Fast-fails if the whitelist or campaign is closed, avoiding infinite wait loops for missing connect buttons.
    """
    if selectors is None:
        selectors = ['.wl-closed', '.campaign-ended', '.ended-message']
    if text_patterns is None:
        text_patterns = ['whitelist is closed', 'campaign ended', 'raffle ended', 'no longer accepting']
        
    for selector in selectors:
        try:
            loc = page.locator(selector).first
            if loc.is_visible():
                msg = loc.inner_text().strip()
                raise Exception(f"HARD_BLOCK: Campaign Ended/Whitelist Closed detected via selector '{selector}': {msg}")
        except Exception as e:
            if "HARD_BLOCK" in str(e):
                raise e

    try:
        body_text = page.evaluate("document.body.innerText || ''").lower()
        for pattern in text_patterns:
            if pattern.lower() in body_text:
                raise Exception(f"HARD_BLOCK: Campaign Ended/Whitelist Closed detected via text pattern: '{pattern}'")
    except Exception as e:
        if "HARD_BLOCK" in str(e):
            raise e

    return False
