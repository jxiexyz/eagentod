# Metadata: Origin Domain: app.afyniti.xyz | Date: 2026-08-18 | Symptom: False positive success claim without verification artifact
import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def verify_action(page: Page, action_selector: str, verification_selector: str, timeout: int = 10000):
    """
    Executes an action and strictly waits for a verification artifact in the DOM.
    Prevents false positive success claims by enforcing explicit state checks.
    """
    try:
        await page.click(action_selector)
        verification_element = await page.wait_for_selector(verification_selector, timeout=timeout, state="visible")
        if not verification_element:
            return {"success": False, "error": f"Verification element '{verification_selector}' not found."}
        artifact_text = await verification_element.text_content()
        return {
            "success": True,
            "artifact_text": artifact_text.strip() if artifact_text else "Element visible"
        }
    except PlaywrightTimeoutError:
        return {"success": False, "error": "Timeout waiting for action or verification."}
    except Exception as e:
        return {"success": False, "error": str(e)}