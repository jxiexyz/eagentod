# Metadata:
# Origin Domain: www.bunnyhood.xyz
# Date: 2026-08-18
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

async def verify_and_extract(page, selector: str, timeout: int = 10000) -> str:
    """Wait for success element and extract artifact text."""
    try:
        el = await page.wait_for_selector(selector, state="visible", timeout=timeout)
        text = await el.text_content()
        if text and text.strip(): return text.strip()
        val = await el.get_attribute("value")
        if val and val.strip(): return val.strip()
        return "[Verified: Element present but empty]"
    except Exception as e:
        raise Exception(f"Verification failed: {selector} not found. {e}")