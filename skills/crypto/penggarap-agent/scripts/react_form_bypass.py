# Metadata: Origin Domain: rewards.svpstars.com, Date: 2026-09-26, Symptom: Quiz form fields reset or fail to register input due to React synthetic events.
import asyncio

async def bypass_fill(page, field_mapping: dict, submit_btn: str = None):
    for sel, val in field_mapping.items():
        await page.wait_for_selector(sel, state='visible', timeout=5000)
        await page.evaluate('''([s, v]) => {
            const el = document.querySelector(s);
            if (!el) return;
            const proto = Object.getPrototypeOf(el);
            const setter = Object.getOwnPropertyDescriptor(proto, 'value')?.set || 
                           Object.getOwnPropertyDescriptor(Object.getPrototypeOf(proto), 'value')?.set;
            if (setter) setter.call(el, v);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }''', [sel, val])
        await asyncio.sleep(0.5)
    
    if submit_btn:
        await page.click(submit_btn)
