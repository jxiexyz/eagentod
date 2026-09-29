# Origin Domain: zygofuture.com
# Date: 2026-08-17
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact (false positive completion).

async def extract_verification_artifact(page, selector: str, timeout: int = 15000) -> str:
    """
    Explicitly waits for and extracts a verification artifact (e.g., success message, Tx hash)
    to prevent false positive success claims.
    """
    try:
        element = await page.wait_for_selector(selector, state="visible", timeout=timeout)
        text = await element.inner_text()
        artifact = text.strip()
        if not artifact:
            raise ValueError("Element found but contained no text.")
        return artifact
    except Exception as e:
        raise RuntimeError(f"Verification extraction failed for '{selector}': {e}")
