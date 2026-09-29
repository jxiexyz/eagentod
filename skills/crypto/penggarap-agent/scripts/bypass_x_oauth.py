# Metadata: inkquills.xyz, 2026-08-24, X OAuth Popup Hang
import asyncio

async def handle_x_oauth(context, page, trigger_selector):
    async with context.expect_page() as new_page_info:
        await page.click(trigger_selector)
    popup = await new_page_info.value
    await popup.wait_for_load_state('networkidle')
    btn = popup.locator('[data-testid="OAuth_Consent_Button"]')
    if await btn.is_visible(timeout=5000):
        await btn.click()
    while not popup.is_closed():
        await asyncio.sleep(0.5)
