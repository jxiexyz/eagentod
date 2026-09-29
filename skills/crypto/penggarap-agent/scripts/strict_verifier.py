# Metadata: Domain: theinitiates.xyz | Date: 2026-08-15 | Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
from typing import Callable, Dict, Any

async def verify_action(page, action_callable: Callable, artifact_selector: str, timeout: int = 15000) -> Dict[str, Any]:
    """
    Executes an action and strictly polls/waits for an expected verification artifact.
    Prevents Worker from assuming success when UI silently fails or hangs.
    """
    try:
        await action_callable()
        element = await page.wait_for_selector(artifact_selector, state='visible', timeout=timeout)
        artifact_text = await element.inner_text()
        return {
            'verified': True,
            'artifact_data': artifact_text.strip() if artifact_text else 'Element visible'
        }
    except Exception as e:
        return {
            'verified': False,
            'error': f'Verification failed. Artifact {artifact_selector} not found. Details: {str(e)}'
        }
