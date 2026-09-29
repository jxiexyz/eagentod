# Origin Domain: tesserapp.org
# Date: 2026-08-19
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

from playwright.async_api import Page, TimeoutError

async def execute_and_verify(page: Page, action_selector: str, verify_selector: str, timeout: int = 15000) -> str:
    """Executes an action and explicitly waits for a verification artifact."""
    try:
        await page.wait_for_selector(action_selector, state="visible", timeout=timeout)
        await page.click(action_selector)
        artifact = await page.wait_for_selector(verify_selector, state="visible", timeout=timeout)
        proof = await artifact.inner_text()
        return proof.strip() if proof else "Artifact found, no text"
    except TimeoutError:
        raise Exception(f"Timeout waiting for verification artifact: {verify_selector}")
