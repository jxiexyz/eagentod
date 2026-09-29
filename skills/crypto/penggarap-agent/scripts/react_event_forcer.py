# Metadata: rewards.svpstars.com, 2026-09-20, Input field not recognizing filled value (React state out of sync)

async def force_react_input(page, selector: str, value: str):
    """Force fills an input and triggers React synthetic events."""
    element = await page.wait_for_selector(selector, state="attached")
    await element.click()
    await page.evaluate('''([el, val]) => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [element, value])
