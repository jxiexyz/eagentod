# Metadata: Origin Domain: hoodgoblins.xyz, Date: 2026-08-27, Symptom: Playwright page.fill() fails to trigger React/SPA state updates for EVM address submission.

async def inject_react_input(page, selector: str, value: str):
    """Bypasses React synthetic events to force input value updates in SPAs."""
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const inputSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        const textSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        const setter = inputSetter || textSetter;
        if (setter) {
            setter.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])
    # Trigger focus and keydown to ensure UI framework registers the change
    await page.focus(selector)
    await page.keyboard.press('Space')
    await page.keyboard.press('Backspace')