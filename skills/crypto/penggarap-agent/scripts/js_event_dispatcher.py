# Metadata: Domain: chatlee.io, Date: 2026-08-21, Symptom: Element not interactable / SPA event block

async def force_js_click(page, selector):
    await page.evaluate('''
        (sel) => {
            const el = document.querySelector(sel);
            if (el) {
                el.click();
                el.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
                el.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
            }
        }
    ''', selector)

async def force_js_type(page, selector, text):
    await page.evaluate('''
        ([sel, txt]) => {
            const el = document.querySelector(sel);
            if (el) {
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                if(nativeInputValueSetter) { nativeInputValueSetter.call(el, txt); }
                else { el.value = txt; }
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
            }
        }
    ''', [selector, text])