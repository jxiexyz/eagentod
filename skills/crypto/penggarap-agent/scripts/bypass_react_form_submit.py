# Metadata: Origin Domain: Generic (app.rally.fun), Date: 2026-08-22, Symptom: React input state ignores standard Playwright page.fill()
import asyncio

async def bypass_react_fill(page, selector: str, value: str):
    """Force React to recognize input values by bypassing synthetic events."""
    await page.wait_for_selector(selector, state="visible", timeout=10000)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def run_whitelist_bypass(page, address_selector: str, evm_address: str, submit_selector: str, social_selectors: list = []):
    """Iterate social tasks, inject EVM address via React bypass, and submit."""
    for sel in social_selectors:
        try:
            await page.wait_for_selector(sel, state="visible", timeout=5000)
            await page.click(sel)
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Skipping {sel}: {e}")
    
    if address_selector and evm_address:
        await bypass_react_fill(page, address_selector, evm_address)
        await asyncio.sleep(1)
        
    if submit_selector:
        await page.wait_for_selector(submit_selector, state="visible", timeout=5000)
        await page.click(submit_selector)
