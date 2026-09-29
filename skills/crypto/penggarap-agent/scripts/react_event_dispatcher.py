# Metadata: Origin Domain: i.mec.me
# Date: 2026-08-25
# Symptom: Playwright fill fails to trigger React/Vue state on registration forms.

async def bypass_react_fill(page, selector: str, value: str):
    await page.wait_for_selector(selector, state='visible')
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error('Element not found');
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])
