# Metadata: hoodgoblins.xyz, 2026-08-27, Playwright fill() fails to trigger React state for EVM input

async def force_react_input(page, selector: str, value: str):
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }""", [selector, value])
