# Metadata: Domain: nibblins.xyz, Date: 2026-08-25, Symptom: Waitlist EVM form submission failure (inferred React synthetic event block)
import asyncio

async def bypass_waitlist_and_submit(page, evm_address: str, task_selector: str = "button:has-text('Follow'), button:has-text('Join')", input_selector: str = "input[placeholder*='0x'], input[type='text']", submit_selector: str = "button[type='submit'], button:has-text('Submit'), button:has-text('Join')"):
    """
    Clicks standard waitlist task buttons, then forces EVM address into React-controlled inputs bypassing synthetic event traps.
    """
    # 1. Execute task buttons (socials/checks) - fail-safe loop
    try:
        task_elements = await page.query_selector_all(task_selector)
        for el in task_elements:
            await el.click(force=True)
            await asyncio.sleep(1.5)
    except Exception:
        pass

    # 2. Inject EVM address deeply into React input
    injected = await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return false;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    }''', [input_selector, evm_address])
    
    if not injected:
        return False
        
    await asyncio.sleep(1)

    # 3. Submit form
    try:
        submit_btn = await page.query_selector(submit_selector)
        if submit_btn:
            await submit_btn.click(force=True)
            await asyncio.sleep(2)
    except Exception:
        pass
        
    return True
