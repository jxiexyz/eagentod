# Metadata: Origin Domain: talesofblobs.com, Date: 2026-08-22, Symptom: EVM address submit failed in session 20260822_003750_a3521d

async def force_react_fill(page, input_selector: str, value: str, submit_selector: str = None):
    await page.wait_for_selector(input_selector, state='attached', timeout=10000)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set || Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        if (setter) setter.call(el, val);
        else el.value = val;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [input_selector, value])
    if submit_selector:
        await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
        await page.click(submit_selector, force=True)
