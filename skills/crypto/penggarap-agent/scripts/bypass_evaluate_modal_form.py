# Metadata: kenjiorigins.com, 2026-08-22, Playwright native click timeout (element not visible) and modal form fill interception
import asyncio

async def bypass_evaluate_modal_form(page, trigger_selector: str, wallet: str, x_user: str, wallet_selector: str, x_selector: str, checkbox_selectors: list, submit_selector: str):
    # Force click trigger via evaluate to bypass visibility/actionability checks
    await page.evaluate('''({selector}) => {
        const btn = document.querySelector(selector);
        if (btn) btn.click();
    }''', {'selector': trigger_selector})
    
    await asyncio.sleep(2)
    
    # Force fill and submit form via evaluate
    result = await page.evaluate('''(data) => {
        const walletInput = document.querySelector(data.wallet_selector);
        const xInput = data.x_selector ? document.querySelector(data.x_selector) : null;
        const submitBtn = document.querySelector(data.submit_selector);
        
        if (walletInput) {
            walletInput.value = data.wallet;
            walletInput.dispatchEvent(new Event('input', { bubbles: true }));
            walletInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        if (xInput && data.x_user) {
            xInput.value = data.x_user;
            xInput.dispatchEvent(new Event('input', { bubbles: true }));
            xInput.dispatchEvent(new Event('change', { bubbles: true }));
        }
        
        if (data.checkbox_selectors) {
            for (const selector of data.checkbox_selectors) {
                const cb = document.querySelector(selector);
                if (cb) {
                    cb.checked = true;
                    cb.dispatchEvent(new Event('change', { bubbles: true }));
                }
            }
        }
        
        if (submitBtn) {
            submitBtn.click();
            return 'Form submitted';
        }
        return 'Submit button not found';
    }''', {
        'wallet': wallet,
        'x_user': x_user,
        'wallet_selector': wallet_selector,
        'x_selector': x_selector,
        'checkbox_selectors': checkbox_selectors,
        'submit_selector': submit_selector
    })
    
    await asyncio.sleep(4)
    return result
