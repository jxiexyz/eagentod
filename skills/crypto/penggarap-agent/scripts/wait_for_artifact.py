# Metadata: Origin Domain: zygofuture.com, Date: 2026-08-17, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

async def execute_and_verify(page, action_selector=None, verify_selector=None, timeout=15000):
    """Executes optional action and strictly waits for verification artifact."""
    if action_selector:
        await page.wait_for_selector(action_selector, state='visible', timeout=timeout)
        await page.click(action_selector)
    
    if not verify_selector:
        raise ValueError('verify_selector is required to extract an artifact.')
        
    try:
        element = await page.wait_for_selector(verify_selector, state='visible', timeout=timeout)
        artifact_text = await page.evaluate('(el) => el.innerText', element)
        
        if not artifact_text or not artifact_text.strip():
            artifact_text = await page.evaluate('(el) => el.value || el.innerHTML', element)
            
        return {'success': True, 'artifact': artifact_text.strip()}
    except Exception as e:
        return {'success': False, 'error': f'Verification artifact {verify_selector} not found: {str(e)}'}
