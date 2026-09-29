# Metadata: 
# Origin Domain: app.afyniti.xyz
# Date: 2026-08-18
# Symptom: hermes -z: no final response was produced (agent hang)

import asyncio

async def safe_goto_and_wait(page, url, timeout_ms=15000):
    """
    Navigates to URL safely, preventing infinite hangs on SPAs or Turnstile loops.
    """
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=timeout_ms)
        await page.wait_for_timeout(3000)
    except Exception as e:
        print(f"Navigation timed out/failed: {e}. Forcing window.stop().")
        await page.evaluate("window.stop()")
    
    try:
        # Clear common blocking modals that trap headless evaluation
        await page.evaluate('''
            document.querySelectorAll('[role="dialog"], .w-screen.h-screen, div[id*="modal"], div[class*="overlay"]').forEach(el => el.remove());
        ''')
    except Exception:
        pass
    
    return True
