# Metadata: Origin Domain: tasks.kryvora.network, Date: 2026-08-18, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.
from playwright.async_api import Page

async def execute_and_verify(page: Page, action_selector: str, verify_selector: str, timeout_ms: int = 5000):
    """
    Executes an action and strictly waits for the verification artifact to appear.
    Prevents false positive task completion reports.
    """
    await page.wait_for_selector(action_selector, state="visible")
    await page.click(action_selector, force=True, delay=100)
    
    try:
        artifact = await page.wait_for_selector(verify_selector, state="visible", timeout=timeout_ms)
        if not artifact:
            raise Exception(f"Action executed but verification artifact '{verify_selector}' not found.")
        return await artifact.inner_text()
    except Exception as e:
        raise Exception(f"Failed to verify action outcome: {str(e)}")
