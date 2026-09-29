# Metadata: Origin Domain: inkpunk.xyz, Date: 2026-08-25, Symptom: React form inputs ignored, social buttons obscured
import asyncio

async def fill_react_input(page, selector: str, value: str):
    """Force React to recognize input changes."""
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
        if (nativeInputValueSetter && nativeInputValueSetter.set) {
            nativeInputValueSetter.set.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }''', [selector, value])

async def force_click(page, selector: str):
    """Bypass overlays for social verification clicks."""
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate('''([sel]) => {
        const el = document.querySelector(sel);
        if (el) el.click();
    }''', [selector])
