# Metadata: Origin Domain: rewards.canopynetwork.org, Date: 2026-08-25, Symptom: Element not interactable / click intercepted on React SPA quests.

async def force_interact(page, selector: str, timeout: int = 5000):
    """Force clicks an element, bypassing Playwright hitability checks and React synthetic event blockers."""
    try:
        await page.wait_for_selector(selector, state='attached', timeout=timeout)
        await page.click(selector, force=True, timeout=timeout)
        return True
    except Exception:
        pass
        
    try:
        element = await page.query_selector(selector)
        if element:
            await page.evaluate('(el) => el.click()', element)
            return True
    except Exception:
        pass
        
    try:
        await page.evaluate('''async (sel) => {
            function findNode(root, sel) {
                let node = root.querySelector(sel);
                if (node) return node;
                for (let child of root.querySelectorAll('*')) {
                    if (child.shadowRoot) {
                        let found = findNode(child.shadowRoot, sel);
                        if (found) return found;
                    }
                }
                return null;
            }
            let btn = findNode(document, sel);
            if (btn) btn.click();
        }''', selector)
        return True
    except Exception as e:
        raise RuntimeError(f"Bypass failed for selector {selector}: {str(e)}")