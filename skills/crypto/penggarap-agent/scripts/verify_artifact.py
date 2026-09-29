# Metadata: Origin Domain: kickhood.fun, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.
from playwright.async_api import Page, TimeoutError

async def extract_verification_artifact(page: Page, success_selector: str, timeout: int = 10000, extract_type: str = 'text') -> str:
    try:
        element = await page.wait_for_selector(success_selector, state='visible', timeout=timeout)
        if not element:
            raise ValueError(f"Verification element '{success_selector}' not found.")
        
        if extract_type == 'text':
            content = await element.inner_text()
        elif extract_type.startswith('attr:'):
            attr_name = extract_type.split(':', 1)[1]
            content = await element.get_attribute(attr_name)
        else:
            content = await element.inner_html()
            
        if not content or not content.strip():
            raise ValueError(f"Verification element '{success_selector}' found but was empty.")
            
        return content.strip()
        
    except TimeoutError:
        raise TimeoutError(f"Timeout ({timeout}ms) waiting for verification artifact at '{success_selector}'.")