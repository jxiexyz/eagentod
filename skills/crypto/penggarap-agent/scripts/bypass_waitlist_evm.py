# Metadata: Origin Domain: nibblins.xyz, Date: 2026-08-25, Symptom: Generic waitlist EVM submission block
import asyncio
from playwright.async_api import Page

async def bypass_waitlist_evm(page: Page, evm_address: str, extra_submit_selectors: list = None):
    input_selectors = [
        "input[placeholder*='0x' i]",
        "input[placeholder*='address' i]",
        "input[placeholder*='wallet' i]",
        "input[name*='address' i]",
        "input[type='text']"
    ]
    
    submit_selectors = [
        "button:has-text('Submit')",
        "button:has-text('Join')",
        "button:has-text('Enter')",
        "button:has-text('Register')",
        "button:has-text('Confirm')",
        "div[role='button']:has-text('Join')"
    ]
    if extra_submit_selectors:
        submit_selectors.extend(extra_submit_selectors)

    filled = False
    for selector in input_selectors:
        try:
            elements = await page.locator(selector).all()
            for el in elements:
                if await el.is_visible():
                    await el.fill(evm_address)
                    filled = True
                    break
        except Exception:
            pass
        if filled:
            break
            
    if not filled:
        raise Exception("Failed to find EVM input field.")

    await page.wait_for_timeout(1000)

    clicked = False
    for selector in submit_selectors:
        try:
            elements = await page.locator(selector).all()
            for el in elements:
                if await el.is_visible():
                    await el.click()
                    clicked = True
                    break
        except Exception:
            pass
        if clicked:
            break
            
    if not clicked:
        raise Exception("Failed to find Submit button.")

    await page.wait_for_timeout(3000)
    return True
