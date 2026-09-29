# Metadata: Origin Domain: inkersnft.xyz, Date: 2026-08-25, Symptom: React SPA form submission failure, social popup blocking

import asyncio

async def fill_react_input(page, selector: str, value: str):
    """Simulates human typing to trigger React onChange events that ignore page.fill()"""
    await page.wait_for_selector(selector, state="visible", timeout=5000)
    await page.click(selector)
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await page.keyboard.type(value, delay=50)

async def bypass_popup_verify(page, selector: str):
    """Clicks social verify buttons and immediately closes the resulting popup to trick frontend state"""
    async with page.expect_popup() as popup_info:
        await page.click(selector)
    popup = await popup_info.value
    await popup.close()
    await asyncio.sleep(1)
