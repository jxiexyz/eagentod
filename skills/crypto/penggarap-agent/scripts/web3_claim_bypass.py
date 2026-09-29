# Metadata: Origin Domain: etherbubu.com, Date: 2026-08-21, Symptom: Web3 Claim button click intercepted or hidden in Shadow DOM.

async def bypass_web3_claim(page, button_text="claim"):
    """
    Recursively finds and clicks a button by text, piercing Shadow DOMs and bypassing overlay intercepts via raw JS evaluation.
    """
    js_code = """
    (searchText) => {
        function findElement(root) {
            const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, null, false);
            let node;
            while (node = walker.nextNode()) {
                if (node.shadowRoot) {
                    const found = findElement(node.shadowRoot);
                    if (found) return found;
                }
                if (node.tagName === 'BUTTON' || node.tagName === 'A' || node.getAttribute('role') === 'button' || node.className.toLowerCase().includes('button')) {
                    if (node.textContent && node.textContent.trim().toLowerCase().includes(searchText.toLowerCase())) {
                        return node;
                    }
                }
            }
            return null;
        }
        const el = findElement(document);
        if (el) {
            el.scrollIntoView({block: 'center', behavior: 'instant'});
            el.click();
            return true;
        }
        return false;
    }
    """
    return await page.evaluate(js_code, button_text)
