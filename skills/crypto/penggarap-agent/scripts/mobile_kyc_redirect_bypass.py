# Origin Domain: i.mec.me
# Date: 2026-08-25
# Symptom: App store/intent redirects interrupting web registration flow

async def bypass_mobile_redirect(page, ref_selector=None, ref_code=None):
    """
    Intercepts and blocks app store redirects, sets mobile viewport, and fills referral code.
    """
    async def handle_route(route):
        url = route.request.url
        if "play.google.com" in url or "apps.apple.com" in url or url.startswith("intent://"):
            await route.abort()
        else:
            await route.continue_()
            
    await page.route("**/*", handle_route)
    await page.set_viewport_size({"width": 390, "height": 844})
    
    if ref_selector and ref_code:
        try:
            await page.wait_for_selector(ref_selector, timeout=5000)
            await page.fill(ref_selector, ref_code)
        except Exception as e:
            print(f"Bypass warning: {ref_selector} not interactable - {e}")
            
    return True
