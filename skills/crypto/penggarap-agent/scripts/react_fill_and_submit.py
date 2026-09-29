# Metadata: commonsmade.com, 2026-08-23, Form submission synthetic event failure

async def react_fill_and_submit(page, input_selector: str, value: str, submit_selector: str = None):
    """Generic bypass for React/Vue inputs that ignore standard page.fill()"""
    await page.wait_for_selector(input_selector, state="visible")
    
    await page.evaluate('''([selector, val]) => {
        const el = document.querySelector(selector);
        if (!el) return;
        el.focus();
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        if (nativeInputValueSetter) {
            nativeInputValueSetter.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [input_selector, value])
    
    if submit_selector:
        await page.wait_for_selector(submit_selector, state="visible", timeout=5000)
        await page.evaluate('''([selector]) => {
            const btn = document.querySelector(selector);
            if (btn) btn.click();
        }''', [submit_selector])
