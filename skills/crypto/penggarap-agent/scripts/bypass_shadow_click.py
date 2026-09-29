# Metadata: Origin Domain: ink-ape.xyz, Date: 2026-08-24, Symptom: Element interception or Waitlist button hidden in Shadow DOM

async def execute_bypass(page, selector: str):
    """
    Generic bypass to force-click an element by piercing Shadow DOMs and ignoring pointer-events/overlays.
    """
    js_script = """(selector) => {
        function findElement(sel, root = document) {
            let el = root.querySelector(sel);
            if (el) return el;
            for (let host of root.querySelectorAll('*')) {
                if (host.shadowRoot) {
                    el = findElement(sel, host.shadowRoot);
                    if (el) return el;
                }
            }
            return null;
        }
        let target = findElement(selector);
        if (target) {
            target.scrollIntoView({block: 'center', behavior: 'instant'});
            target.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
            return true;
        }
        return false;
    }"""
    
    try:
        # Attempt native Playwright force click first
        await page.click(selector, force=True, timeout=3000)
    except Exception:
        # Fallback to aggressive JS injection
        success = await page.evaluate(js_script, selector)
        if not success:
            raise Exception(f"Bypass failed: Element '{selector}' not found in main or Shadow DOM.")
