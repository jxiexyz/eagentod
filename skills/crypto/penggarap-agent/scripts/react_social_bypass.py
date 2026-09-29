# Metadata: bubblebuns.xyz, 2026-08-27, React form input not registering and external social links hanging browser

async def bypass_react_input(page, selector: str, value: str):
    """Force React to recognize input by dispatching native events."""
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def safe_social_click(page, selector: str):
    """Prevent social/TG links from opening new tabs and hanging execution."""
    await page.evaluate('''([sel]) => {
        const el = document.querySelector(sel);
        if (el) {
            el.removeAttribute('target');
            el.click();
        }
    }''', [selector])
