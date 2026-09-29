# Metadata: Domain: nibblins.xyz, Date: 2026-08-26, Symptom: Failure to identify BSC address input and social verification buttons.
import asyncio

async def bypass_social_campaign(page, bsc_address: str):
    try:
        address_input = page.locator('input[placeholder*="0x"], input[placeholder*="address" i], input[type="text"]')
        if await address_input.count() > 0:
            await address_input.first.fill(bsc_address)
    except Exception as e:
        print(f"Address input error: {e}")

    try:
        buttons = page.locator('button:has-text("Submit"), button:has-text("Join"), button:has-text("Verify")')
        for i in range(await buttons.count()):
            if await buttons.nth(i).is_visible():
                await buttons.nth(i).click()
                await asyncio.sleep(2)
    except Exception as e:
        print(f"Button click error: {e}")
        
    return True
