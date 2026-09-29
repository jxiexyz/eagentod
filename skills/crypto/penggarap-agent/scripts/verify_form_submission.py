# Metadata: Origin Domain: docs.google.com | Date: 2026-08-19 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from playwright.async_api import Page

async def verify_submission(page: Page, success_text: str = "Your response has been recorded.", timeout: int = 5000) -> str:
    """
    Generic form submission verifier.
    Waits for specific success text to appear and returns it as a verification artifact.
    """
    try:
        locator = page.get_by_text(success_text, exact=False).first
        await locator.wait_for(state="visible", timeout=timeout)
        artifact = await locator.inner_text()
        return f"VERIFIED: Found '{artifact}' at {page.url}"
    except Exception as e:
        raise Exception(f"Verification failed. Text '{success_text}' not found within {timeout}ms. Current URL: {page.url}. Error: {str(e)}")
