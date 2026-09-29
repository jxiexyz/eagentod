# Metadata:
# Origin Domain: zygofuture.com
# Date: 2026-08-17
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio

async def verify_and_extract_artifact(page, success_selector: str, artifact_selector: str = None, timeout: int = 15000):
    """
    Waits for a success state and extracts the verification artifact.
    """
    try:
        await page.wait_for_selector(success_selector, state='visible', timeout=timeout)
        if artifact_selector:
            element = await page.query_selector(artifact_selector)
            if element:
                artifact = await element.inner_text()
                if not artifact:
                    artifact = await element.get_attribute('href')
                if not artifact:
                    artifact = await element.get_attribute('value')
                return {'success': True, 'artifact': artifact.strip() if artifact else None}
        return {'success': True, 'artifact': 'Success selector found, no extraction selector provided.'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
