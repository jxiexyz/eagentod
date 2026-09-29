# Metadata: Domain: intersticedigital.io, Date: 2026-08-22, Symptom: Interstitial automation block timeout
import asyncio

async def bypass_interstitial(page, target_selector="iframe", timeout_ms=15000):
    """Generic bypass for interstitial challenge pages."""
    try:
        await page.wait_for_load_state('domcontentloaded')
        challenge = page.locator(target_selector).first
        if await challenge.is_visible(timeout=5000):
            box = await challenge.bounding_box()
            if box:
                await page.mouse.click(box['x'] + box['width']/2, box['y'] + box['height']/2)
                await asyncio.sleep(2)
        await page.wait_for_load_state('networkidle', timeout=timeout_ms)
        return True
    except Exception as e:
        print(f"Bypass error: {e}")
        return False
