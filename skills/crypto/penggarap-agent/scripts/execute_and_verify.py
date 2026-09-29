# Origin Domain: kickhood.fun
# Date: 2026-08-19
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact (false positive completion)

from playwright.async_api import Page, TimeoutError

async def execute_and_verify(page: Page, action_callback, verify_selector: str, timeout: int = 15000) -> str:
    """
    Executes an action and strictly waits for a verification element to appear.
    Returns the text content of the verification artifact, preventing phantom success.
    """
    try:
        await action_callback(page)
        element = await page.wait_for_selector(verify_selector, state="visible", timeout=timeout)
        if element:
            text = await element.text_content()
            return text.strip() if text else "VERIFIED_BUT_EMPTY_TEXT"
    except TimeoutError:
        pass
    except Exception:
        pass
    return ""