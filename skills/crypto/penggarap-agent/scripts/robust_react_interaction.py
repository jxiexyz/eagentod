# Metadata: Origin Domain: actionmodel.com, Date: 2026-08-26, Symptom: Playwright input ignored by React state

async def bypass_react_fill(page, selector, text):
    """Bypass React synthetic events using native setters."""
    await page.evaluate('''([sel, txt]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found: " + sel);
        const proto = Object.getPrototypeOf(el);
        const desc = Object.getOwnPropertyDescriptor(proto, 'value') || Object.getOwnPropertyDescriptor(Object.getPrototypeOf(proto), 'value');
        if (!desc || !desc.set) throw new Error("No native setter found for " + sel);
        desc.set.call(el, txt);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, text])

async def stealth_click(page, selector):
    """Click via native JS to bypass interception checks."""
    await page.evaluate('''sel => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Element not found: " + sel);
        el.click();
    }''', selector)