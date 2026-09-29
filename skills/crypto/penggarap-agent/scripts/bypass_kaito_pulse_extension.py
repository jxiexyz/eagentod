# Metadata: kaito.ai, 2026-08-21, Kaito Pulse Extension Onboarding Block
import asyncio

async def bypass(page, *args, **kwargs):
    print("[*] Applying Kaito Pulse Extension API mock...")
    
    async def intercept_onboarding(route):
        print(f"[*] Intercepted Kaito Pulse check: {route.request.url}")
        await route.fulfill(
            status=200,
            content_type="application/json",
            body='{"data":{"onboarded":true,"status":"success"},"success":true,"code":200,"message":"success"}'
        )

    # Intercept backend verification calls for the extension
    await page.route("**/api/v1/extension/onboarding/status*", intercept_onboarding)
    await page.route("**/api/v1/extension/status*", intercept_onboarding)
    
    # Force enable any visually disabled 'Continue' buttons
    await page.evaluate("""() => {
        setInterval(() => {
            document.querySelectorAll('button').forEach(btn => {
                if (btn.disabled || btn.getAttribute('aria-disabled') === 'true') {
                    btn.disabled = false;
                    btn.removeAttribute('disabled');
                    btn.removeAttribute('aria-disabled');
                    btn.style.opacity = '1';
                }
            });
        }, 1000);
    }""")
    
    print("[+] Kaito Pulse bypass applied.")
    return True
