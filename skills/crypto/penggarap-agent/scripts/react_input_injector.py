# Metadata: Origin Domain: whitelist.brokedealershq.xyz, Date: 2026-08-27, Symptom: Fails to trigger React/Vue synthetic events on web3 form input fields.

async def inject_react_input(page, selector: str, value: str):
    """Injects text into React/Vue controlled inputs bypassing synthetic event blocks."""
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error(`Selector not found: ${sel}`);
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        if (nativeInputValueSetter) {
            nativeInputValueSetter.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])
