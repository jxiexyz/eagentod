# Metadata: kaito.ai, 2026-08-21, React OTP inputs dropping values or triggering invalid state due to synthetic event issues
import asyncio
from playwright.async_api import Page

async def fill_react_otp(page: Page, code: str, input_selector: str = 'input[data-input-otp="true"]'):
    """
    Bypasses React synthetic events for OTP input arrays by dispatching native events
    and forcing React state updates per character.
    """
    await page.wait_for_selector(input_selector, state="visible", timeout=10000)
    
    await page.evaluate('''([sel, codeStr]) => {
        const inputs = document.querySelectorAll(sel);
        if (inputs.length >= codeStr.length) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value');
            for(let i=0; i<codeStr.length; i++) {
                if (nativeInputValueSetter && nativeInputValueSetter.set) {
                    nativeInputValueSetter.set.call(inputs[i], codeStr[i]);
                } else {
                    inputs[i].value = codeStr[i];
                }
                inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[i].dispatchEvent(new Event('change', { bubbles: true }));
            }
        }
    }''', [input_selector, code])
    
    await asyncio.sleep(1)
    return True