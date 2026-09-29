# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-18, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from playwright.async_api import Page, TimeoutError

async def click_and_verify_artifact(page: Page, action_selector: str, success_selector: str, timeout: int = 15000):
    """
    Clicks an element and explicitly waits for a verification artifact (success state) to appear.
    Prevents false-positive success claims by enforcing strict state transition checks.
    """
    try:
        action_el = page.locator(action_selector).first
        await action_el.wait_for(state="visible", timeout=timeout)
        await action_el.click()
        
        success_el = page.locator(success_selector).first
        await success_el.wait_for(state="visible", timeout=timeout)
        
        artifact_text = await success_el.inner_text()
        return {"success": True, "artifact": artifact_text.strip()}
        
    except TimeoutError:
        return {"success": False, "error": f"Timeout waiting for artifact '{success_selector}' after clicking '{action_selector}'."}
    except Exception as e:
        return {"success": False, "error": str(e)}
