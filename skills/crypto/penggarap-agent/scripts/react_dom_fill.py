# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-24, Symptom: Playwright page.fill() fails to trigger React state updates on vouch forms/inputs.

async def force_react_fill(page, selector: str, text: str):
    """
    Sets input value bypassing React's synthetic events by invoking the native setter.
    Useful when standard Playwright fill() leaves the internal React state empty.
    """
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error(`Element not found: ${sel}`);
        
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(el, val);
        
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, text])

async def force_js_click(page, selector: str):
    """
    Forces a click via DOM evaluation to bypass invisible overlays or strict hit-testing.
    """
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate('''sel => {
        const el = document.querySelector(sel);
        if (!el) throw new Error(`Element not found: ${sel}`);
        el.click();
    }''', selector)
