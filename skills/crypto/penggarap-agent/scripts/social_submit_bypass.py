# Metadata: Origin Domain: conso.xyz, Date: 2026-08-26, Symptom: Fails to complete social tasks and submit BSC address due to popups blocking execution flow.

import asyncio

async def bypass_social_and_submit(page, address: str, input_selector: str, submit_btn_selector: str, social_btn_selectors: list):
    """Generic bypass for social task sequences (handles/closes popups) and submits an address."""
    for sel in social_btn_selectors:
        try:
            # Intercept and close social/TG popups to keep focus on main page
            async with page.expect_event("popup", timeout=3000) as popup_info:
                await page.click(sel, force=True)
            popup = await popup_info.value
            await popup.close()
        except Exception:
            # Fallback if it didn't open a popup or timed out
            try:
                await page.click(sel, force=True)
            except:
                pass
        await asyncio.sleep(1.5)
    
    # Proceed to form submission
    await page.wait_for_selector(input_selector, timeout=5000, state="visible")
    await page.fill(input_selector, address)
    await asyncio.sleep(1)
    await page.click(submit_btn_selector, force=True)
    await asyncio.sleep(3)
