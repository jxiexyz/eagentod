# Metadata
# Origin Domain: di.xyz (generic Web3 check-in)
# Date: 2026-08-27
# Symptom: Input fills or clicks failing due to React synthetic events, shadow DOM, or overlapping overlays.

import asyncio

async def robust_checkin_submit(page, input_selector: str, input_value: str, submit_selector: str = None):
    try:
        await page.evaluate('''() => {
            document.querySelectorAll('*').forEach(el => {
                if (window.getComputedStyle(el).zIndex > 1000) { el.style.display = 'none'; }
            });
        }''')
        
        await page.wait_for_selector(input_selector, state='attached', timeout=5000)
        await page.evaluate('''([selector, val]) => {
            const el = document.querySelector(selector);
            if (!el) return;
            el.focus();
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
            if (nativeSetter) {
                nativeSetter.call(el, val);
            } else {
                el.value = val;
            }
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }''', [input_selector, input_value])
        
        await asyncio.sleep(1)
        
        if submit_selector:
            await page.wait_for_selector(submit_selector, state='attached', timeout=5000)
            await page.evaluate('''([selector]) => {
                const el = document.querySelector(selector);
                if (el) el.click();
            }''', [submit_selector])
            
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
