# Origin Domain: tesserapp.org
# Date: 2026-08-21
# Specific Symptom: Clicks intercepted by invisible overlays or React synthetic events in Tesserapp raffle UI.

import asyncio

async def execute_bypass(page, target_selector="button:has-text('Enter')"):
    try:
        await page.wait_for_selector(target_selector, state="attached", timeout=10000)
        elements = await page.locator(target_selector).element_handles()
        for el in elements:
            is_vis = await el.is_visible()
            if is_vis:
                await page.evaluate("(element) => element.click()", el)
                await asyncio.sleep(1)
        return True
    except Exception as e:
        print(f"Bypass error: {e}")
        return False
