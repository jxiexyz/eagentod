# Metadata: Origin Domain: inkvikings.xyz, Date: 2026-08-24, Symptom: Waitlist form automation timeout/locator failure

import asyncio
from playwright.async_api import Page

async def bypass_waitlist(page: Page, email: str = "", wallet: str = ""):
    try:
        for sel in ["input[type='email']", "input[name*='email' i]", "input[placeholder*='email' i]"]:
            loc = page.locator(sel)
            if await loc.count() > 0 and email:
                await loc.first.fill(email)
                break

        for sel in ["input[name*='wallet' i]", "input[placeholder*='0x' i]"]:
            loc = page.locator(sel)
            if await loc.count() > 0 and wallet:
                await loc.first.fill(wallet)
                break

        for sel in ["button:has-text('Apply')", "button:has-text('Join')", "button:has-text('Submit')"]:
            loc = page.locator(sel)
            if await loc.count() > 0:
                await loc.first.click()
                break

        await page.wait_for_timeout(3000)
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
