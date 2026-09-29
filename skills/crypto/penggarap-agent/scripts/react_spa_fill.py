# Metadata: Origin Domain: playground.rialo.io, Date: 2026-08-24, Symptom: React SPA form/invite code input failure (synthetic events blocking standard fill)
import asyncio

async def react_spa_fill(page, selector: str, value: str):
    """
    Bypasses React synthetic event blocking by setting the native value setter 
    and dispatching input/change events directly via CDP/JS evaluation.
    """
    await page.wait_for_selector(selector, state='visible', timeout=15000)
    
    # Focus and click the element to ensure it is active
    await page.click(selector)
    
    # Type value to trigger basic keyboard events
    await page.type(selector, value, delay=50)
    
    # Force React to recognize the change via native prototype setter
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        let lastValue = el.value;
        el.value = val;
        let event = new Event('input', { bubbles: true });
        // React 16+ overrides the native setter
        let tracker = el._valueTracker;
        if (tracker) {
            tracker.setValue(lastValue);
        }
        el.dispatchEvent(event);
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])
    
    await asyncio.sleep(0.5)
    return True