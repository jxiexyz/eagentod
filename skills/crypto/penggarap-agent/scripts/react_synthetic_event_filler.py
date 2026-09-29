# Metadata: Generic React SPA, 2026-08-24, Playwright fill() fails to trigger React state updates

async def react_fill(page, selector: str, value: str):
    """
    Fills an input and explicitly dispatches React-compatible updates
    so that synthetic event listeners pick up the change.
    """
    await page.locator(selector).fill(value)
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const lastValue = el.value;
        el.value = val;
        const event = new Event("input", { bubbles: true });
        const tracker = el._valueTracker;
        if (tracker) {
            tracker.setValue(lastValue);
        }
        el.dispatchEvent(event);
    }''', [selector, value])
