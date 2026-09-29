# Metadata: Origin Domain: join.actionmodel.com | Date: 2026-08-27 | Symptom: Blocked social task and wallet form submission (React/Vue synthetic events missing)
import asyncio

async def bypass_social_form(page, bsc_address, wallet_selector="input[type='text'], input[placeholder*='address' i], input[placeholder*='BSC' i]"):
    """
    Bypasses standard input blocks on React/Vue social airdrop forms.
    Forces value entry and dispatches synthetic events.
    """
    try:
        await page.wait_for_selector(wallet_selector, state='attached', timeout=5000)
        
        # Force value setter for React/Vue DOM elements
        await page.evaluate(f'''(selector, address) => {{
            const el = document.querySelector(selector);
            if (el) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeInputValueSetter.call(el, address);
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}''', wallet_selector, bsc_address)
        
        # Fallback raw typing if evaluate didn't trigger UI updates
        await page.locator(wallet_selector).first.click(force=True)
        await page.keyboard.press('Space')
        await page.keyboard.press('Backspace')
        
        # Auto-click generic submit buttons
        submit_selectors = ["button:has-text('Submit')", "button:has-text('Join')", "button:has-text('Claim')", "div[role='button']:has-text('Submit')"]
        for btn in submit_selectors:
            if await page.locator(btn).count() > 0:
                await page.locator(btn).first.click(force=True)
                await asyncio.sleep(2)
                break
                
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
