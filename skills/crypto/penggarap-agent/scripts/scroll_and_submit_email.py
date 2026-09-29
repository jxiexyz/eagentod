# Metadata: Origin Domain: app.bitrobot.ai, Date: 2026-08-22, Symptom: Waitlist form requires scroll and generic email submit
import asyncio

async def bypass(page, email: str, input_selector: str = "input[type='email'], input[placeholder*='mail' i]", submit_selector: str = "button[type='submit'], button:has-text('Join'), button:has-text('Submit')"):
    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    await page.wait_for_timeout(1500)
    await page.wait_for_selector(input_selector, state="visible", timeout=10000)
    await page.fill(input_selector, email)
    await page.click(submit_selector)
    await page.wait_for_timeout(2000)
    return True
