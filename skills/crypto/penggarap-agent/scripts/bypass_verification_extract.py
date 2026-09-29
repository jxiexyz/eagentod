# Metadata: 
# Origin Domain: withspout.com
# Date: 2026-08-17
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

async def extract_verification_artifact(page, success_selector="text='Success', text='Confirmed', .success-message, [data-testid='success']", extract_attribute="innerText", timeout=15000):
    """
    Waits for a generic success indicator and extracts the text/attribute as a verifiable artifact.
    """
    try:
        element = await page.wait_for_selector(success_selector, timeout=timeout, state="visible")
        if not element:
            raise Exception("Verification element not found.")
        
        if extract_attribute == "innerText":
            artifact = await element.inner_text()
        else:
            artifact = await element.get_attribute(extract_attribute)
            
        return artifact.strip() if artifact else "Verification element found but empty."
    except Exception as e:
        return f"Verification failed: {str(e)}"