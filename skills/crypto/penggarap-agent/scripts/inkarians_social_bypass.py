# Metadata: Domain: inkarians.xyz, Date: 2026-08-25, Symptom: Missing social click dispatch and address form fill
import asyncio
from playwright.async_api import Page

async def execute_social_drop_bypass(page: Page, address: str):
    # 1. Dispatch social clicks to satisfy local state checks
    socials = page.locator("a[href*='t.me'], a[href*='twitter.com'], a[href*='x.com']")
    count = await socials.count()
    for i in range(count):
        elem = socials.nth(i)
        if await elem.is_visible():
            await elem.click(modifiers=["Control"])
            await asyncio.sleep(1)

    # 2. Fill Address
    inputs = page.locator("input")
    input_count = await inputs.count()
    for i in range(input_count):
        elem = inputs.nth(i)
        ph = await elem.get_attribute("placeholder") or ""
        name = await elem.get_attribute("name") or ""
        if "0x" in ph or "address" in ph.lower() or "bsc" in ph.lower() or "wallet" in name.lower():
            await elem.fill(address)
            await asyncio.sleep(0.5)
            break

    # 3. Submit
    submit = page.locator("button", has_text="Submit").or_(page.locator("button", has_text="Join"))
    if await submit.count() > 0:
        await submit.first.click()
        await asyncio.sleep(2)
