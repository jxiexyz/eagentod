# Metadata: inkersnft.xyz, 2026-08-24, React input fill failure for EVM address
import asyncio

async def react_fill(page, selector: str, value: str):
    """Bypass React synthetic events by setting native value and dispatching Event."""
    await page.wait_for_selector(selector, state="visible", timeout=10000)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Selector not found: " + sel);
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        const setter = el.tagName.toLowerCase() === 'textarea' ? nativeTextAreaValueSetter : nativeInputValueSetter;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])