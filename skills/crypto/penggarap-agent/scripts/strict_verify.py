# Metadata: Origin Domain: hedgelords.cash, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

async def execute_and_verify(page, action_fn, success_selector, timeout=15000):
    """
    Executes an action and strictly waits for a verifiable success artifact in the DOM.
    Prevents false positive success claims.
    
    Args:
        page: Playwright page object.
        action_fn: Async function containing the action (e.g., form submission, click).
        success_selector: CSS selector for the success message or verification artifact.
        timeout: Max time to wait for the artifact in milliseconds.
    """
    await action_fn()
    
    try:
        element = await page.wait_for_selector(success_selector, state='visible', timeout=timeout)
        if not element:
            raise RuntimeError(f"Verification selector '{success_selector}' not found.")
            
        artifact = await element.inner_text()
        if not artifact or artifact.strip() == '':
            raise RuntimeError("Artifact element found, but it is empty.")
            
        return artifact.strip()
    except Exception as e:
        raise RuntimeError(f"Verification failed. The action may not have succeeded. Error: {str(e)}")
