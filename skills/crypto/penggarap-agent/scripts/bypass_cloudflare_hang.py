# Origin Domain: cero.finance
# Date: 2026-08-18
# Symptom: hermes -z: no final response was produced (timeout/hang)

import asyncio

async def bypass_hang(page, timeout=30000):
    """
    Resolves page hangs caused by Cloudflare Turnstile or stuck loading overlays.
    """
    try:
        cf_count = await page.locator('#turnstile-wrapper, .cf-turnstile, iframe[src*="cloudflare"]').count()
        if cf_count > 0:
            await page.wait_for_load_state('networkidle', timeout=timeout)
            await asyncio.sleep(3)
        
        overlays = ['.loading-overlay', '#loader', '#splash', '[id*="loader"]', '[class*="loading"]']
        for overlay in overlays:
            loc = page.locator(overlay)
            if await loc.count() > 0 and await loc.first.is_visible():
                await loc.evaluateAll('els => els.forEach(e => e.remove())')
                
    except Exception:
        pass
        
    return True
