# Metadata: Origin: points.concrete.xyz | Date: 2026-08-18 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

from playwright.async_api import Page, TimeoutError

async def verify_artifact(page: Page, selector: str, timeout: int = 15000) -> str:
    """
    Wait for a specific DOM element that proves transaction/claim success and return its text.
    """
    try:
        el = await page.wait_for_selector(selector, state="visible", timeout=timeout)
        if not el:
            return ""
        text = await el.inner_text()
        return text.strip() or "[Element Visible - No Text]"
    except TimeoutError:
        raise Exception(f"Verification failed: {selector} not found within {timeout}ms")
