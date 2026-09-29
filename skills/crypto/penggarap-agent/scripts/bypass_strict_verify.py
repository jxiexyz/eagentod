# Metadata: Origin Domain: rally.fun | Date: 2026-08-18 | Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

async def execute_and_verify(page, action_selector: str, verify_selector: str, timeout: int = 15000):
    """
    Executes an action and strictly requires a verification artifact to appear in the DOM.
    Prevents false positive success claims by the worker.
    """
    await page.locator(action_selector).click()
    
    try:
        verify_element = page.locator(verify_selector).first
        await verify_element.wait_for(state='visible', timeout=timeout)
        artifact_text = await verify_element.inner_text()
        if not artifact_text.strip():
            raise ValueError("Verification artifact element found but text is empty.")
        return artifact_text.strip()
    except Exception as e:
        raise Exception(f"Verification failed. Expected artifact '{verify_selector}' not found or invalid. Original error: {str(e)}")
