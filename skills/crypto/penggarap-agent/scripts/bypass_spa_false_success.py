# Metadata: Origin Domain: s.kaito.ai, Date: 2026-08-19, Symptom: Worker claims success but provides NO valid VERIFICATION artifact (false positive)
from playwright.sync_api import Page, TimeoutError

def strict_action_and_verify(page: Page, action_selector: str, verify_selector: str, timeout: int = 15000) -> bool:
    """
    Generic bypass for SPA forms that silently fail or swallow clicks.
    Forces a trusted click and STRICTLY waits for a verification artifact in the DOM.
    """
    try:
        page.wait_for_selector(action_selector, state="visible", timeout=timeout)
        element = page.locator(action_selector).first
        element.scroll_into_view_if_needed()
        element.click(delay=150)
        
        page.wait_for_selector(verify_selector, state="visible", timeout=timeout)
        return True
    except TimeoutError:
        return False
    except Exception as e:
        print(f"Strict verify failed: {e}")
        return False
