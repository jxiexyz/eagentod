# Metadata: Origin Domain: tsukinft.xyz, Date: 2026-08-19, Symptom: Fake success / No verification artifact
import asyncio
from playwright.async_api import Page, TimeoutError

async def execute_and_verify(page: Page, action_selector: str, success_selector: str, timeout: int = 30000) -> str:
    """
    Executes an action and strictly waits for a verification artifact in the DOM.
    """
    await page.click(action_selector)
    
    try:
        element = await page.wait_for_selector(success_selector, state="visible", timeout=timeout)
        if not element:
            raise Exception(f"Verification element '{success_selector}' not found.")
        
        proof = await element.inner_text()
        return proof.strip()
    except TimeoutError:
        raise Exception(f"Verification '{success_selector}' timed out.")
