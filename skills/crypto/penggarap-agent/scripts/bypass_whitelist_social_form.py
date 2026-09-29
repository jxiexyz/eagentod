# Metadata: Origin Domain: talesofblobs.com, Date: 2026-08-22, Symptom: Whitelist EVM input and social task automation failure
import asyncio
from playwright.async_api import Page

async def execute_bypass(page: Page, evm_address: str, form_selector: str = "form"):
    """
    Universal bypass for crypto whitelist forms requiring EVM address and social clicks.
    Forces React/Vue state updates via raw event dispatch.
    """
    try:
        # 1. Fill EVM address with React state bypass
        input_locators = [
            "input[placeholder*='0x' i]", 
            "input[name*='wallet' i]", 
            "input[name*='address' i]",
            "input[type='text']"
        ]
        
        input_element = None
        for loc in input_locators:
            elements = page.locator(loc)
            if await elements.count() > 0:
                for i in range(await elements.count()):
                    if await elements.nth(i).is_visible():
                        input_element = elements.nth(i)
                        break
            if input_element:
                break
                
        if input_element:
            await input_element.focus()
            await input_element.fill(evm_address)
            await input_element.evaluate("el => { el.dispatchEvent(new Event('input', {bubbles: true})); el.dispatchEvent(new Event('change', {bubbles: true})); }")
            
        # 2. Click social triggers (Follow/Join/Verify)
        social_keywords = ["Follow", "Join", "Verify", "Connect", "Check"]
        for keyword in social_keywords:
            btns = page.locator(f"button:has-text('{keyword}')")
            for i in range(await btns.count()):
                btn = btns.nth(i)
                if await btn.is_visible() and not await btn.is_disabled():
                    await btn.click(force=True)
                    await asyncio.sleep(1)
                    
        # 3. Submit
        submit_btn = page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Enter')").first
        if await submit_btn.is_visible() and not await submit_btn.is_disabled():
            await submit_btn.click(force=True)
            
        return True
    except Exception as e:
        print(f"[Bypass Error] {e}")
        return False
