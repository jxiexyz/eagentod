# Metadata: Origin: billiz.xyz | Date: 2026-08-19 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.
import asyncio
from playwright.async_api import Page, TimeoutError

async def perform_verified_action(page: Page, action_selector: str, verification_selector: str, timeout: int = 10000):
    """
    Clicks an element and strictly waits for a verification artifact to appear.
    Raises an exception if the verification fails, preventing false successes.
    """
    await page.wait_for_selector(action_selector, state="visible", timeout=timeout)
    await page.click(action_selector)
    
    try:
        element = await page.wait_for_selector(verification_selector, state="visible", timeout=timeout)
        artifact = await element.inner_text()
        if not artifact:
            artifact = await element.get_attribute("value")
        return artifact.strip() if artifact else "Verification element confirmed present."
    except TimeoutError:
        raise Exception(f"Action on {action_selector} executed, but verification {verification_selector} failed to appear.")