# Origin Domain: zygofuture.com
# Date: 2026-08-17
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact (false positive).

from playwright.async_api import Page

async def click_and_verify(page: Page, click_selector: str, verify_selector: str, timeout: int = 15000) -> str:
    """
    Executes a click and strictly waits for a verification artifact to appear.
    Returns the text of the artifact as verifiable proof.
    """
    await page.click(click_selector)
    try:
        element = await page.wait_for_selector(verify_selector, state="visible", timeout=timeout)
        text = await element.inner_text()
        if not text:
            text = await element.get_attribute("value")
        return text.strip() if text else "Verification element found but empty"
    except Exception as e:
        raise RuntimeError(f"Action completed but verification artifact '{verify_selector}' failed to appear. {e}")