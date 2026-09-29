# Origin Domain: Generic (Triggered by s.kaito.ai)
# Date: 2026-08-19
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

import asyncio

async def extract_verification(page, success_selectors=None, timeout=10000):
    """
    Wait for and extract a verification artifact after an action to ensure proof of success.
    """
    default_selectors = [
        "text='Success'",
        "text='Claimed'",
        "text='Verified'",
        "text='Congratulations'",
        ".toast-success",
        "[role='alert']",
        ".SnackbarItem-message"
    ]
    
    selectors = success_selectors if success_selectors else default_selectors
    
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout)
    except Exception:
        pass
        
    artifact = None
    for selector in selectors:
        try:
            element = await page.wait_for_selector(selector, state='visible', timeout=2000)
            if element:
                text = await element.inner_text()
                artifact = {"selector": selector, "text": text.strip()}
                break
        except Exception:
            continue
            
    if not artifact:
        # Fallback to basic page state if explicit artifact isn't found
        artifact = {
            "fallback": True,
            "url": page.url,
            "title": await page.title()
        }
        
    return artifact
