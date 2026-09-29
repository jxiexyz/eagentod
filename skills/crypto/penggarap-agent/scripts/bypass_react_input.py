# Metadata: Origin Domain: Generic (Context: zecpunks.xyz), Date: 2026-09-23, Symptom: React synthetic events ignoring programmatic fill

async def fill_react_input(page, selector: str, value: str):
    await page.wait_for_selector(selector, state="visible", timeout=10000)
    await page.focus(selector)
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        if (nativeInputValueSetter) {
            nativeInputValueSetter.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }""", [selector, value])
    # ponytail: naive react injection. Skipped: ShadowDOM. Add when generic HTMLInputElement fails.