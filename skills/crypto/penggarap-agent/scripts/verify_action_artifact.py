# Metadata: Domain: points.concrete.xyz, Date: 2026-08-18, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.
import asyncio
from playwright.async_api import Page, TimeoutError

async def execute_and_verify(page: Page, action_selector: str, artifact_selector: str, timeout: int = 10000) -> str:
    """
    Executes an action and STRICTLY waits for a verification artifact to prevent false positive successes.
    """
    try:
        await page.click(action_selector)
        artifact = await page.wait_for_selector(artifact_selector, state="visible", timeout=timeout)
        if not artifact:
            raise Exception(f"Artifact '{artifact_selector}' not found after action.")
        return (await artifact.inner_text()).strip()
    except TimeoutError:
        raise Exception(f"Timeout waiting for verification artifact '{artifact_selector}'.")