# Origin Domain: nft.retium.org
# Date: 2026-08-22
# Specific Symptom: Playwright unable to interact with Web3 modal/faucet buttons due to Shadow DOM or overlay interception (session cd6997)

async def force_shadow_click(page, selector: str, text_fallback: str = ""):
    """
    Bypass Playwright interception/visibility blockers by using deep JS traversal.
    Finds elements piercing Shadow DOMs and clicks them natively.
    """
    js_script = '''([sel, txt]) => {
        function deepSearch(node) {
            if (!node) return null;
            if (sel && node.matches && node.matches(sel)) return node;
            if (txt && node.textContent && node.textContent.trim().toLowerCase().includes(txt.toLowerCase()) && ['BUTTON', 'A', 'DIV'].includes(node.tagName)) {
                return node;
            }
            if (node.shadowRoot) {
                let found = deepSearch(node.shadowRoot);
                if (found) return found;
            }
            for (let child of (node.children || [])) {
                let found = deepSearch(child);
                if (found) return found;
            }
            return null;
        }
        let el = deepSearch(document);
        if (el) {
            el.click();
            return true;
        }
        return false;
    }'''
    
    try:
        return await page.evaluate(js_script, [selector, text_fallback])
    except Exception as e:
        print(f"Deep click bypass failed: {e}")
        return False
