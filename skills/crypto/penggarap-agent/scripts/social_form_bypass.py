# Metadata: Origin Domain: farmcorn.fun, Date: 2026-08-22, Symptom: Social task form submission and wallet input automation failure
import asyncio
from playwright.async_api import Page

async def bypass_social_form(
    page: Page, 
    twitter_username: str, 
    wallet_address: str, 
    twitter_selector: str = "input[placeholder*='Twitter'], input[name*='twitter'], input[placeholder*='@']", 
    wallet_selector: str = "input[placeholder*='Solana'], input[placeholder*='SOL'], input[name*='wallet']", 
    task_selector: str = "a[href*='twitter.com'], a[href*='x.com'], button:has-text('Follow'), button:has-text('Retweet')", 
    submit_selector: str = "button:has-text('Submit'), button:has-text('Join'), button[type='submit']"
):
    await page.wait_for_load_state('domcontentloaded')
    
    # 1. Fill Twitter Username
    twitter_input = page.locator(twitter_selector).first
    if await twitter_input.is_visible(timeout=5000):
        await twitter_input.fill(twitter_username)
        await page.wait_for_timeout(500)

    # 2. Fill Wallet Address
    wallet_input = page.locator(wallet_selector).first
    if await wallet_input.is_visible(timeout=5000):
        await wallet_input.fill(wallet_address)
        await page.wait_for_timeout(500)

    # 3. Simulate Social Task Clicks (Open in background to preserve state)
    tasks = page.locator(task_selector)
    count = await tasks.count()
    for i in range(count):
        try:
            await tasks.nth(i).click(modifiers=['Control'], force=True)
            await page.wait_for_timeout(1000)
        except Exception:
            continue

    # 4. Submit Form
    submit_btn = page.locator(submit_selector).first
    if await submit_btn.is_visible(timeout=5000):
        await submit_btn.click(force=True)
        await page.wait_for_timeout(2000)

    return True
