# Metadata: Origin Domain: event.neosoul.ai, Date: 2026-08-21, Symptom: Web3 wallet connection, invite code input, and social task onboarding failures.
import asyncio
from playwright.async_api import Page

async def run_bypass(page: Page, invite_code: str = None):
    try:
        connect_btns = await page.locator("button:has-text('Connect'), button:has-text('Wallet')").all()
        if connect_btns:
            await connect_btns[0].click()
            await asyncio.sleep(2)
            await page.locator("text=MetaMask, text=Injected, text=Browser Wallet").first.click(force=True)
            await asyncio.sleep(3)

        if invite_code:
            invite_input = page.locator("input[placeholder*='code' i], input[name*='invite' i], input[type='text']")
            if await invite_input.count() > 0:
                await invite_input.first.fill(invite_code)
                await asyncio.sleep(1)
                submit_btn = page.locator("button:has-text('Submit'), button:has-text('Confirm'), button:has-text('Enter')")
                if await submit_btn.count() > 0:
                    await submit_btn.first.click()
                    await asyncio.sleep(2)

        twitter_btn = page.locator("button:has-text('Twitter'), button:has-text('X'), a:has-text('Connect X')")
        if await twitter_btn.count() > 0:
            await twitter_btn.first.click()
            await asyncio.sleep(2)

        return {"status": "success", "message": "Bypass executed successfully."}
    except Exception as e:
        return {"status": "error", "error": str(e)}
