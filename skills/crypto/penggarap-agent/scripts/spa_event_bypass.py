# Metadata: Origin Domain: puffins.fun, Date: 2026-08-22, Specific Symptom: Standard playwright clicks and text inputs are ignored by React/Vue synthetic event listeners during task completion and address submission.

async def bypass_spa_events(page, selector: str, text: str = None):
    """Dispatch native events to bypass React/Vue synthetic event traps for form submission."""
    await page.wait_for_selector(selector, state='attached', timeout=10000)
    await page.evaluate('''([sel, txt]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        
        // Native Click Bypass
        ['pointerdown', 'mousedown', 'mouseup', 'pointerup', 'click'].forEach(e => {
            el.dispatchEvent(new MouseEvent(e, {bubbles: true, cancelable: true, view: window}));
        });
        
        // React/Vue Input Bypass
        if (txt !== null) {
            el.value = txt;
            const tracker = el._valueTracker;
            if (tracker) tracker.setValue(String(el.value || ''));
            el.dispatchEvent(new Event('input', {bubbles: true}));
            el.dispatchEvent(new Event('change', {bubbles: true}));
        }
    }''', [selector, text])
    return True
