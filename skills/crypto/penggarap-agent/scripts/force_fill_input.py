# Metadata:
# Origin Domain: commonsmade.com
# Date: 2026-08-23
# Symptom: Input fields not registering text due to React/Vue synthetic event handlers missing standard Playwright inputs.

async def force_fill_input(page, selector: str, value: str):
    """
    Forces an input field to accept a value and triggers native JS events to bypass React/Vue state blockers.
    """
    await page.wait_for_selector(selector, state="visible", timeout=15000)
    await page.fill(selector, "")
    await page.type(selector, value, delay=50)
    
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (el) {
            el.value = val;
            // Hack to bypass React16+ synthetic event tracker
            const tracker = el._valueTracker;
            if (tracker) tracker.setValue('');
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }''', [selector, value])
