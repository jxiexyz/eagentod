# Metadata: Origin: justbanners.art, Date: 2026-08-22, Symptom: Element click intercepted by overlay or hidden in Shadow DOM

async def force_click(page, selector: str):
    """Bypass overlays and Shadow DOM boundaries by dispatching native JS events."""
    js_snippet = """
    (sel) => {
        const elements = document.querySelectorAll(sel);
        let target = elements.length ? elements[0] : null;
        if (!target) {
            const allNodes = document.querySelectorAll('*');
            for (const node of allNodes) {
                if (node.shadowRoot) {
                    const shadowEl = node.shadowRoot.querySelector(sel);
                    if (shadowEl) { target = shadowEl; break; }
                }
            }
        }
        if (target) {
            target.scrollIntoView({behavior: 'instant', block: 'center'});
            target.dispatchEvent(new MouseEvent('click', {
                bubbles: true, 
                cancelable: true, 
                view: window
            }));
        } else {
            throw new Error('Selector not found: ' + sel);
        }
    }
    """
    await page.evaluate(js_snippet, selector)
