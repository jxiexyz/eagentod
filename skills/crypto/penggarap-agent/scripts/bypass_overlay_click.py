# Metadata: Domain: krakensprimates.site, Date: 2026-08-26, Symptom: Interaction blocked by overlays or non-standard DOM elements in limited quests

async def bypass_click(page, selector: str, timeout: int = 5000) -> bool:
    """
    Attempts standard click, falls back to JS click to bypass pointer-events/overlays.
    """
    try:
        element = await page.wait_for_selector(selector, state="attached", timeout=timeout)
        if element:
            try:
                await element.click(timeout=timeout)
                return True
            except Exception:
                # Fallback to Javascript click to bypass overlays intercepting the click
                await page.evaluate("(sel) => document.querySelector(sel).click()", selector)
                return True
    except Exception as e:
        print(f"Bypass click failed for {selector}: {e}")
    return False
