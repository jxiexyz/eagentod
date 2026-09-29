# Metadata: Origin Domain: tesserapp.org, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

from playwright.async_api import Page, TimeoutError

async def extract_verification_artifact(page: Page, selector: str, timeout: int = 15000) -> str:
    """
    Wait for a specific success element and extract its text or attribute as a verification artifact.
    """
    try:
        element = await page.wait_for_selector(selector, timeout=timeout, state="visible")
        if not element:
            return ""
        
        href = await element.get_attribute("href")
        if href:
            return href
        
        text = await element.inner_text()
        return text.strip()
    except TimeoutError:
        return ""
