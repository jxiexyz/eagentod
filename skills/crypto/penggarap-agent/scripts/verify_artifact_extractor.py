# Metadata
# Origin Domain: points.concrete.xyz
# Date: 2026-08-18
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def extract_verification_artifact(page: Page, artifact_selector: str, timeout: int = 15000, attribute: str = None) -> str:
    """
    Waits for and extracts a verification artifact to prove task completion.
    Prevents false positive success claims by raising an exception if missing.
    """
    try:
        element = await page.wait_for_selector(artifact_selector, timeout=timeout, state="visible")
        if not element:
            raise ValueError(f"Verification artifact '{artifact_selector}' not found in DOM.")
        
        if attribute:
            artifact = await element.get_attribute(attribute)
        else:
            artifact = await element.inner_text()
            
        if not artifact or not artifact.strip():
            raise ValueError(f"Artifact element '{artifact_selector}' found, but content is empty.")
            
        return artifact.strip()
    except PlaywrightTimeoutError:
        raise TimeoutError(f"Timeout ({timeout}ms) waiting for verification artifact: {artifact_selector}")
