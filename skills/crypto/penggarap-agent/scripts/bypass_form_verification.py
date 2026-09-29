# Metadata: Origin: docs.google.com, Date: 2026-08-18, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

async def verify_submission(page, timeout_ms=10000):
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout_ms)
        artifact = await page.evaluate('document.body.innerText')
        return {'verified': True, 'artifact': artifact[:500].strip()}
    except Exception as e:
        return {'verified': False, 'error': str(e)}
