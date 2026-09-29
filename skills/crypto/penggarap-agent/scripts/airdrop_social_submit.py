# Metadata: Domain: bafoontown.wtf, Date: 2026-08-25, Symptom: Social task target=_blank hangs and form submission blocks
import asyncio
from playwright.async_api import Page

async def bypass_and_submit(page: Page, address: str, address_selector: str = "input"): 
    # Prevent window.open from hanging the automation on social tasks
    await page.evaluate("window.open = function() { return null; };")
    
    # Force click social links without waiting for navigation
    for keyword in ['twitter.com', 'x.com', 't.me']:
        links = await page.locator(f"a[href*='{keyword}']").all()
        for link in links:
            await link.click(force=True, no_wait_after=True)
            await asyncio.sleep(0.5)
            
    # Fill the EVM address
    target_input = page.locator(address_selector).first
    await target_input.wait_for(state="attached", timeout=5000)
    await target_input.fill(address, force=True)
    await page.keyboard.press("Enter")
    
    # Fallback: force click generic submit buttons
    submit_btns = await page.locator("button").all()
    for btn in submit_btns:
        text = await btn.text_content()
        if text and any(k in text.lower() for k in ['submit', 'join', 'claim', 'enter', 'register']):
            await btn.click(force=True, no_wait_after=True)
            break