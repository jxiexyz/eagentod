# Metadata: Origin app.rally.fun, Date 2026-08-26, Symptom Element click intercepted or Shadow DOM / React synthetic event failure

async def execute_bypass(page, selector: str):
    """
    Finds an element by piercing through shadow DOMs and dispatches React-compatible pointer/mouse events.
    """
    js_code = """
    (sel) => {
        const findElement = (selector, root) => {
            let el = root.querySelector(selector);
            if (el) return el;
            for (const child of root.querySelectorAll('*')) {
                if (child.shadowRoot) {
                    let res = findElement(selector, child.shadowRoot);
                    if (res) return res;
                }
            }
            return null;
        };
        
        const target = findElement(sel, document);
        if (!target) throw new Error('Selector not found: ' + sel);
        
        target.scrollIntoView({block: 'center', inline: 'center'});
        
        const events = ['pointerdown', 'mousedown', 'pointerup', 'mouseup', 'click'];
        events.forEach(ev => 
            target.dispatchEvent(new MouseEvent(ev, { bubbles: true, cancelable: true, view: window }))
        );
        
        return true;
    }
    """
    await page.evaluate(js_code, selector)
