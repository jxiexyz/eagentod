# Metadata: Domain: talesofblobs.com, Date: 2026-08-21, Symptom: React synthetic events not firing on standard fill / Form submission blocked
async def react_force_fill(page, selector: str, value: str):
    """Forces a React input to accept a value by bypassing SyntheticEvent wrappers, setting the native prototype setter, and dispatching Event."""
    await page.wait_for_selector(selector, state="attached")
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error(`Selector not found: ${sel}`);
        
        const nativeInputSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        const nativeTextAreaSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        
        if (nativeInputSetter && el.tagName === 'INPUT') {
            nativeInputSetter.call(el, val);
        } else if (nativeTextAreaSetter && el.tagName === 'TEXTAREA') {
            nativeTextAreaSetter.call(el, val);
        } else {
            el.value = val;
        }
        
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        el.dispatchEvent(new Event('blur', { bubbles: true }));
    }''', [selector, value])