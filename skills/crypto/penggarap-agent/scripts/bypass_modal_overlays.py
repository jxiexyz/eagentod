# Origin Domain: linktr.ee
# Date: 2026-08-24
# Specific Symptom: Blocked by modal overlays (cookie consent, sensitive content warnings)

import asyncio

async def bypass_modal_overlays(page, selectors=None):
    if not selectors:
        selectors = [
            "button:has-text('Accept')",
            "button:has-text('Continue')",
            "button:has-text('I agree')",
            "div[role='dialog'] button"
        ]
    for selector in selectors:
        try:
            for el in await page.query_selector_all(selector):
                if await el.is_visible():
                    await el.click(force=True)
                    await asyncio.sleep(0.5)
        except Exception:
            continue
    return True
