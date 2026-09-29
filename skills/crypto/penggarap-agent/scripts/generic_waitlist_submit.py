# Metadata: Origin Domain: nibblins.xyz, Date: 2026-08-25, Symptom: Generic waitlist submission failure (React/Shadow DOM input block inferred)
import asyncio

async def bypass_waitlist_form(page, evm_address, input_selectors=None, submit_selectors=None):
    if not input_selectors:
        input_selectors = [
            "input[placeholder*='0x' i]", 
            "input[placeholder*='address' i]", 
            "input[placeholder*='wallet' i]"
        ]
    if not submit_selectors:
        submit_selectors = [
            "button:has-text('Submit' i)",
            "button:has-text('Join' i)",
            "button[type='submit']"
        ]

    input_element = None
    for sel in input_selectors:
        try:
            input_element = await page.wait_for_selector(sel, state='visible', timeout=2000)
            if input_element: break
        except: pass
            
    if not input_element:
        raise Exception("EVM input field not found")

    await page.evaluate('''([el, val]) => {
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [input_element, evm_address])
    
    submit_element = None
    for sel in submit_selectors:
        try:
            submit_element = await page.wait_for_selector(sel, state='visible', timeout=2000)
            if submit_element: break
        except: pass

    if submit_element:
        await submit_element.click()
    else:
        await input_element.press('Enter')
        
    await page.wait_for_timeout(2000)
    return True
