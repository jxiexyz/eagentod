# Metadata: Origin Domain: sohonft.site, Date: 2026-08-21, Symptom: Interaction failure on whitelist form / element intercepted

async def smart_click(page, selector: str, timeout: int = 5000):
    """
    Attempts standard click, JS click, and shadow DOM piercing click.
    """
    try:
        await page.wait_for_selector(selector, state="attached", timeout=timeout)
    except Exception:
        pass

    # Strategy 1: Standard Playwright click
    try:
        await page.click(selector, timeout=2000)
        return True
    except Exception:
        pass
        
    # Strategy 2: JS Evaluation click (bypasses overlays and event interceptors)
    try:
        await page.evaluate(f"document.querySelector('{selector}').click()")
        return True
    except Exception:
        pass
        
    # Strategy 3: Deep shadow DOM click (WalletConnect / Dynamic.xyz widgets)
    try:
        js_code = """
        (selector) => {
            function findElement(root, sel) {
                if (root.querySelector(sel)) return root.querySelector(sel);
                for (let el of root.querySelectorAll('*')) {
                    if (el.shadowRoot) {
                        let found = findElement(el.shadowRoot, sel);
                        if (found) return found;
                    }
                }
                return null;
            }
            let el = findElement(document, selector);
            if (el) { el.click(); return true; }
            return false;
        }
        """
        result = await page.evaluate(js_code, selector)
        if (result) return True
    except Exception:
        pass
        
    return False
