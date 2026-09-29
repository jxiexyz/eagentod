# Metadata: Origin Domain: thor.savethelife.io, Date: 2026-08-25, Symptom: Social signup and wallet submission timeouts
import asyncio
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

async def handle_crypto_social_signup(page: Page, address: str):
    try:
        await page.wait_for_selector('iframe', timeout=3000)
        for frame in page.frames:
            if 'cloudflare' in frame.url or 'turnstile' in frame.url:
                await page.wait_for_timeout(4000)
    except PlaywrightTimeoutError:
        pass

    wallet_inputs = ['input[name="wallet"]', 'input[name="address"]', 'input[placeholder*="BSC"]', 'input[placeholder*="address" i]']
    for selector in wallet_inputs:
        try:
            if await page.is_visible(selector, timeout=2000):
                await page.fill(selector, address)
                break
        except Exception:
            continue

    social_links = ['a[href*="t.me"]', 'a[href*="twitter.com"]', 'a[href*="x.com"]']
    for selector in social_links:
        elements = await page.query_selector_all(selector)
        for el in elements:
            await page.evaluate('(element) => element.removeAttribute("target")', el)
            await el.evaluate('(element) => element.dispatchEvent(new MouseEvent("click", {bubbles: true}))')
            await page.wait_for_timeout(1000)

    try:
        await page.click('button[type="submit"], button:has-text("Sign Up"), button:has-text("Submit"), button:has-text("Join")', timeout=3000)
        await page.wait_for_load_state('networkidle', timeout=5000)
    except PlaywrightTimeoutError:
        pass

    return True
