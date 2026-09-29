# Metadata:
# Origin Domain: minibroker.xyz
# Date: 2026-08-18
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from playwright.async_api import Page, TimeoutError

async def extract_verification_artifact(page: Page, success_selector: str = None, success_text: str = None, timeout: int = 15000):
    """
    Waits for a success state and extracts a verification artifact to prove completion.
    """
    artifact = None
    try:
        if success_selector:
            element = await page.wait_for_selector(success_selector, state="visible", timeout=timeout)
            artifact = await element.inner_text()
        elif success_text:
            element = page.locator(f"text={success_text}").first
            await element.wait_for(state="visible", timeout=timeout)
            artifact = await element.inner_text()
        else:
            await page.wait_for_load_state("networkidle", timeout=timeout)
            artifact = await page.locator("body").inner_text()
            artifact = artifact[:500] + "..." if len(artifact) > 500 else artifact
            
    except TimeoutError:
        artifact = await page.locator("body").inner_text()
        artifact = "TIMEOUT WAITING FOR SUCCESS. Current text: " + artifact[:500]
        
    return artifact
