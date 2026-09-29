# Origin Domain: onchainsketches.xyz
# Date: 2026-08-27
# Symptom: Cannot fill EVM address or click submit due to React synthetic events masking input state.

from playwright.async_api import Page

async def fill_react_evm_form(page: Page, evm_address: str, input_selector: str = "input", submit_selector: str = "button"):
    await page.evaluate('''([address, inpSel]) => {
        const inputs = Array.from(document.querySelectorAll(inpSel));
        const target = inputs.find(i => (i.placeholder || '').toLowerCase().includes('0x')) || inputs[0];
        if (target) {
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set || Object.getOwnPropertyDescriptor(Object.getPrototypeOf(target), 'value')?.set;
            if (nativeSetter) nativeSetter.call(target, address);
            else target.value = address;
            target.dispatchEvent(new Event('input', { bubbles: true }));
            target.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }''', [evm_address, input_selector])
    
    await page.wait_for_timeout(500)
    
    await page.evaluate('''([btnSel]) => {
        const btns = Array.from(document.querySelectorAll(btnSel));
        const target = btns.find(b => (b.textContent || '').match(/submit|join|whitelist|enter|register/i)) || btns[0];
        if (target) target.click();
    }''', [submit_selector])
