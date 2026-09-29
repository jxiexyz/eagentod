# Metadata: Origin Domain: digitsbt.ngrndrewards.com, Date: 2026-08-23, Symptom: Wallet connect button unclickable due to Shadow DOM isolation

def bypass_shadow_dom_click(page, button_text: str):
    """
    Traverses open shadow roots to find and click a button by its text content.
    Useful for Web3Modal, Privy, or Dynamic UI elements hidden from standard selectors.
    """
    js_code = """
    (text) => {
        function findElement(root) {
            const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, null, false);
            let node;
            while (node = walker.nextNode()) {
                if (node.shadowRoot) {
                    const found = findElement(node.shadowRoot);
                    if (found) return found;
                }
                if (node.tagName !== 'SCRIPT' && node.tagName !== 'STYLE') {
                    let hasText = Array.from(node.childNodes).some(n => 
                        n.nodeType === Node.TEXT_NODE && n.textContent.trim().toLowerCase() === text.toLowerCase()
                    );
                    if (hasText) return node;
                }
            }
            return null;
        }
        const el = findElement(document);
        if (el) {
            el.scrollIntoView();
            el.click();
            return true;
        }
        return false;
    }
    """
    return page.evaluate(js_code, button_text)
