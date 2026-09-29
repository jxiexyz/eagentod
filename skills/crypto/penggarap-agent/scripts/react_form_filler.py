# Metadata: Origin Domain: thor.savethelife.io, Date: 2026-08-24, Symptom: Playwright page.fill() fails to trigger React state updates for referral/auth inputs
import asyncio

async def set_react_input(page, selector: str, value: str):
    """
    Bypasses React synthetic event traps by calling the native HTMLInputElement value setter
    and manually dispatching bubbled input/change events.
    """
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found: " + sel);
        
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
            window.HTMLInputElement.prototype,
            "value"
        ).set;
        
        nativeInputValueSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])
