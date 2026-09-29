# Metadata: Origin Domain: 4bitink.xyz, Date: 2026-08-24, Symptom: React synthetic event ignoring Playwright page.fill() and intercepted clicks

import asyncio

async def bypass_spa_form(page, input_selector: str, value: str, submit_selector: str = None):
    """
    Forces text into a React/Web3 input field and clicks the submit button, bypassing overlays.
    """
    await page.wait_for_selector(input_selector, state="attached", timeout=15000)
    
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set;
        if (setter) setter.call(el, val);
        el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [input_selector, value])
    
    await page.locator(input_selector).fill(value, force=True)
    
    if submit_selector:
        await page.wait_for_selector(submit_selector, state="attached")
        await page.evaluate('''([sel]) => {
            const el = document.querySelector(sel);
            if (el) el.click();
        }''', [submit_selector])
        await page.locator(submit_selector).click(force=True)
        
    return True
