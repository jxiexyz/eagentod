# Metadata: Domain: tesserapp.org, Date: 2026-08-21, Symptom: Element not found or clicks intercepted by Shadow DOM / React wrappers

async def shadow_piercing_click(page, selector: str):
    """
    Finds an element by traversing shadow DOM boundaries and dispatches native events
    to bypass React synthetic event suppression.
    """
    js_script = """
    (selector) => {
        function findDeep(sel, root = document) {
            let el = root.querySelector(sel);
            if (el) return el;
            for (let e of root.querySelectorAll('*')) {
                if (e.shadowRoot) {
                    let match = findDeep(sel, e.shadowRoot);
                    if (match) return match;
                }
            }
            return null;
        }
        let target = findDeep(selector);
        if (!target) throw new Error('Element not found: ' + selector);
        ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'].forEach(ev => {
            target.dispatchEvent(new MouseEvent(ev, {bubbles: true, cancelable: true, view: window}));
        });
    }
    """
    await page.evaluate(js_script, selector)