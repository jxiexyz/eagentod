# Metadata: Domain: zygofuture.com, Date: 2026-08-17, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact

async def capture_verification_artifact(page, selector, timeout_ms=5000):
    element = page.locator(selector).first
    await element.wait_for(state="visible", timeout=timeout_ms)
    return await element.screenshot(type="jpeg", quality=70)
