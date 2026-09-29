# Metadata: Domain: i.mec.me, Date: 2026-08-25, Symptom: Task requires mobile app download and biometric Face/ID KYC

async def execute_bypass(page, **kwargs):
    """
    Aborts tasks requiring mobile app downloads and physical biometric KYC,
    as these cannot be completed via standard headless web automation.
    """
    print('[Worker] Aborting: Target strictly requires mobile app and biometric KYC.')
    return {'status': 'aborted', 'reason': 'App download and biometric KYC unsupported'}
