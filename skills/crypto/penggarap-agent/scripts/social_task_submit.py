# Metadata: Domain: inksideout.site, Date: 2026-08-27, Symptom: Fails to complete social tasks and submit BSC address
import asyncio

async def run_bypass(page, bsc_address: str = ""):
    await page.evaluate("window.open = () => null;")
    
    for text in ["Join", "Follow", "Start", "Verify", "Check"]:
        locators = page.locator(f"button:has-text('{text}'), a:has-text('{text}')")
        count = await locators.count()
        for i in range(count):
            try:
                if await locators.nth(i).is_visible():
                    await locators.nth(i).click(timeout=2000)
                    await asyncio.sleep(1)
            except Exception:
                continue

    if bsc_address:
        address_input = page.locator("input[placeholder*='0x' i], input[placeholder*='address' i], input[placeholder*='BSC' i]")
        if await address_input.count() > 0:
            await address_input.first.fill(bsc_address)

    submit = page.locator("button:has-text('Submit'), button:has-text('Claim')")
    if await submit.count() > 0:
        await submit.first.click(timeout=2000)
        
    return True