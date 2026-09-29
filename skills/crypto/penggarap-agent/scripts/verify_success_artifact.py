# Metadata: Origin Domain: tesserapp.org, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact (false positive)
import asyncio
from typing import List

async def verify_success_artifact(page, success_selectors: List[str], timeout: int = 10000) -> str:
    """
    Forces the worker to actually find a success artifact (e.g., 'Joined', checkmark, toast popup)
    before returning success. Prevents false-positive completions.
    """
    for selector in success_selectors:
        try:
            element = await page.wait_for_selector(selector, state="visible", timeout=timeout)
            if element:
                text = await element.inner_text()
                return f"Verified artifact via '{selector}': {text.strip() or '[Element Visible]'}"
        except Exception:
            continue
            
    # ponytail: Dump HTML if all selectors fail. Add DOM parsing if specific error text is needed.
    raise Exception(f"VERIFICATION FAILED: None of the success selectors {success_selectors} appeared on page.")