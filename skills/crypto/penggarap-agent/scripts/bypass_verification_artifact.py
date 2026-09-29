# Metadata: Origin: hedgelords.cash, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.

async def extract_verification_artifact(page, success_selector=None, timeout=10000):
    """Waits for explicit DOM/network state change to extract proof of success."""
    try:
        if success_selector:
            await page.wait_for_selector(success_selector, state='visible', timeout=timeout)
            element = page.locator(success_selector).first
            return {'verified': True, 'artifact': await element.inner_text()}
        
        await page.wait_for_load_state('networkidle', timeout=timeout)
        return {'verified': True, 'artifact': f'URL: {page.url} | Title: {await page.title()}'}
    except Exception as e:
        return {'verified': False, 'error': str(e)}