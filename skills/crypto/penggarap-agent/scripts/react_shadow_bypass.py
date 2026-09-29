# Metadata:
# Origin Domain: waitlist.gte.xyz
# Date: 2026-08-20
# Symptom: Playwright interactability checks failing or React synthetic events not registering input.

async def force_fill_react(page, selector: str, value: str):
    """
    Fills an input by bypassing React's synthetic event wrappers and Playwright's visibility checks.
    """
    await page.evaluate('''({selector, value}) => {
        let el = document.querySelector(selector);
        if (!el) {
            const node = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (node) el = node;
        }
        if (!el) throw new Error('Element not found: ' + selector);
        
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        const nativeTextareaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set;
        
        if (el.tagName.toLowerCase() === 'textarea' && nativeTextareaValueSetter) {
            nativeTextareaValueSetter.call(el, value);
        } else if (nativeInputValueSetter) {
            nativeInputValueSetter.call(el, value);
        } else {
            el.value = value;
        }
        
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', {'selector': selector, 'value': value})

async def force_click(page, selector: str):
    """
    Force clicks an element via native JS, bypassing Playwright's actionability checks.
    """
    await page.evaluate('''({selector}) => {
        let el = document.querySelector(selector);
        if (!el) {
            const node = document.evaluate(selector, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (node) el = node;
        }
        if (!el) throw new Error('Element not found: ' + selector);
        el.click();
    }''', {'selector': selector})