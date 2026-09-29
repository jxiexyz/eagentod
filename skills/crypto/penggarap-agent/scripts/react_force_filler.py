# Metadata: Origin Domain: Generic (app.meridian.xyz), Date: 2026-08-22, Symptom: React synthetic event blocking EVM address form submission and social button clicks

async def force_fill_and_click(page, input_selector: str, value: str, button_selector: str = None):
    """
    Forces React to recognize input changes and clicks a target button bypassing strict interactability checks.
    """
    try:
        await page.wait_for_selector(input_selector, state='attached', timeout=5000)
        await page.evaluate('''([sel, val]) => {
            const el = document.querySelector(sel);
            if (!el) return;
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            if (nativeInputValueSetter) {
                nativeInputValueSetter.call(el, val);
            } else {
                el.value = val;
            }
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }''', [input_selector, value])
        
        if button_selector:
            await page.evaluate('''([sel]) => {
                const el = document.querySelector(sel);
                if (el) el.click();
            }''', [button_selector])
            
        return True
    except Exception as e:
        print(f"Bypass script error: {e}")
        return False
