# Metadata: Origin Domain: hoodstarz.xyz, Date: 2026-08-15, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def verify_and_extract_artifact(page: Page, selector: str, timeout: int = 10000) -> str:
    """
    Waits for a specific verification artifact in the DOM and extracts its text or value.
    Throws an exception if not found, preventing false positive success claims.
    """
    try:
        element = await page.wait_for_selector(selector, state="visible", timeout=timeout)
        if not element:
            raise ValueError(f"Artifact selector '{selector}' resolved to None.")
        
        text_content = await element.text_content()
        if text_content and text_content.strip():
            return text_content.strip()
        
        value = await element.get_attribute("value")
        if value and value.strip():
            return value.strip()
            
        raise ValueError(f"Artifact found at '{selector}' but contained no extractable text or value.")
        
    except PlaywrightTimeoutError:
        raise TimeoutError(f"Verification artifact '{selector}' did not appear within {timeout}ms.")
