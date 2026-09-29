# Metadata: Origin: dollclub.xyz, Date: 2026-08-17, Symptom: hermes -z timeout / hanging page load
import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def safe_goto(page: Page, url: str, timeout_ms: int = 15000):
    """
    Navigates safely, averting networkidle hangs that cause hermes -z timeouts.
    Halts loading aggressively if timeout is hit but DOM is present.
    """
    try:
        await page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
    except PlaywrightTimeoutError:
        print(f"[safe_goto] Timeout reached for {url}, forcing window.stop()")
        try:
            await page.evaluate("window.stop()")
        except Exception:
            pass
    
    await asyncio.sleep(2)
    
    # Check for Cloudflare/antibot walls that stall automation
    if await page.locator(".cf-turnstile, #cf-please-wait, #challenge-running").count() > 0:
        print("[safe_goto] Cloudflare/Antibot detected, allowing stabilization...")
        await asyncio.sleep(5)
        
    return page
