# Metadata: Origin Domain: Generic (teogiwa.com), Date: 2026-08-24, Symptom: React form synthetic event blocks and obscured social tasks

async def force_react_fill(page, selector: str, value: str):
    """Bypasses React synthetic events by using native input setters to force value recognition."""
    await page.wait_for_selector(selector, state='attached', timeout=5000)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def force_click_elements(page, selectors: list):
    """Force clicks elements (like social tasks) bypassing pointer-events:none or overlays."""
    for sel in selectors:
        try:
            await page.evaluate('''([s]) => {
                const el = document.querySelector(s);
                if (el) el.click();
            }''', [sel])
        except Exception:
            pass