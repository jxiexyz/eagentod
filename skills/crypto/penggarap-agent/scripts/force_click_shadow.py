# Metadata: Origin Domain: rewards.canopynetwork.org | Date: 2026-08-25 | Symptom: Element not clickable / Blocked by overlay / Shadow DOM barrier

async def force_click(page, selector: str):
    """Force clicks bypassing overlays and piercing Shadow DOM (WalletConnect/Dynamic UI)."""
    await page.evaluate('''(sel) => {
        function findElement(root, s) {
            let el = root.querySelector(s);
            if (el) return el;
            for (let child of root.querySelectorAll('*')) {
                if (child.shadowRoot) {
                    let res = findElement(child.shadowRoot, s);
                    if (res) return res;
                }
            }
            return null;
        }
        let target = findElement(document, sel);
        if (target) {
            target.scrollIntoView({block: 'center', behavior: 'instant'});
            target.click();
            return true;
        }
        throw new Error(`Element not found: ${sel}`);
    }''', selector)