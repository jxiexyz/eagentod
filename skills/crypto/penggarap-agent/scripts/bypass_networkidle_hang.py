# Origin Domain: app.rally.fun (generic)
# Date: 2026-08-17
# Specific Symptom: hermes -z: no final response was produced (hang due to networkidle/polling)

async def force_page_load(page, url, timeout_ms=15000):
    """Forces page load without waiting for networkidle, aborting infinite spinners."""
    page.set_default_navigation_timeout(timeout_ms)
    page.set_default_timeout(timeout_ms)
    try:
        await page.goto(url, wait_until='domcontentloaded')
    except Exception:
        pass
    
    try:
        await page.evaluate('window.stop()')
    except Exception:
        pass
        
    return True
