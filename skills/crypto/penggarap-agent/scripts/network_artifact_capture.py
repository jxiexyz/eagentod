# Metadata:
# Origin Domain: zygofuture.com
# Date: 2026-08-17
# Specific Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio
import re

async def execute_and_verify(page, action_callback, api_pattern=r'(claim|submit|verify|success|graphql)', timeout=15000):
    """
    Executes an action and awaits matching API response to extract network artifact.
    Bypasses missing DOM updates or ephemeral toast notifications by reading network payloads.
    """
    async with page.expect_response(
        lambda response: re.search(api_pattern, response.url, re.IGNORECASE) and response.status in (200, 201),
        timeout=timeout
    ) as response_info:
        await action_callback()
        
    response = await response_info.value
    try:
        return await response.json()
    except Exception:
        return await response.text()
