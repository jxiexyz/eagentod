# Origin Domain: theofficenft.io
# Date: 2026-08-27
# Symptom: Missing EVM submission and whitelist task verification failures due to React-controlled form inputs

import asyncio
from playwright.async_api import Page

async def submit_whitelist_form(page: Page, evm_address: str, address_selectors: list = None, submit_selectors: list = None):
    if address_selectors is None:
        address_selectors = ["input[placeholder*='0x']", "input[name*='wallet']", "input[name*='address']", "input[type='text']"]
    if submit_selectors is None:
        submit_selectors = ["button[type='submit']", "button:has-text('Submit')", "button:has-text('Register')", "button:has-text('Join')"]

    try:
        # 1. Handle Generic Social Tasks (Click verifies/checks)
        tasks = await page.locator("button:has-text('Verify'), button:has-text('Check'), button:has-text('Follow')").all()
        for task in tasks:
            if await task.is_visible():
                await task.click(force=True)
                await asyncio.sleep(1)

        # 2. Find and fill EVM address
        input_found = False
        for sel in address_selectors:
            if await page.locator(sel).count() > 0:
                # React 16+ input bypass
                await page.evaluate(f'''(address, selector) => {{
                    const input = document.querySelector(selector);
                    if (input) {{
                        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                        nativeInputValueSetter.call(input, address);
                        input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                        input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}''', evm_address, sel)
                await page.fill(sel, evm_address, force=True)
                input_found = True
                break
        
        if not input_found:
            print("EVM address input not found on page.")
            return False

        # 3. Submit Form
        for sub_sel in submit_selectors:
            if await page.locator(sub_sel).count() > 0:
                await page.locator(sub_sel).first.click(force=True)
                await asyncio.sleep(2)
                return True
        
        return False
    except Exception as e:
        print(f"Whitelist bypass execution failed: {e}")
        return False
