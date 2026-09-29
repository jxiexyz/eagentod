# Metadata: Domain: pad.chaingpt.org, Date: 2026-08-27, Symptom: React input state ignoring standard fill or buttons being intercepted by overlays.

async def react_fill(page, selector: str, value: str):
    """Bypass React state locking to fill inputs."""
    await page.wait_for_selector(selector, state='attached', timeout=10000)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const tracker = el._valueTracker;
        if (tracker) tracker.setValue('');
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        if (setter) setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def force_click(page, selector: str):
    """Force click an element ignoring overlays/interceptions."""
    await page.wait_for_selector(selector, state='attached', timeout=10000)
    await page.evaluate('''sel => {
        const el = document.querySelector(sel);
        if (el) el.click();
    }''', selector)