# Metadata: Origin Domain: inkarians.xyz | Date: 2026-08-25 | Symptom: Social task tabs blocking flow, React input drops address
import asyncio

async def bypass_social_and_submit(page, task_selectors: list, input_selector: str, submit_value: str, submit_btn: str = None):
    for sel in task_selectors:
        try:
            await page.evaluate(f'''(s) => {{
                document.querySelectorAll(s).forEach(el => {{
                    el.removeAttribute('target');
                    el.addEventListener('click', e => e.preventDefault());
                }});
            }}''', sel)
            await page.click(sel, force=True, timeout=3000)
            await asyncio.sleep(1)
        except Exception:
            pass
            
    try:
        await page.evaluate(f'''(s, v) => {{
            let el = document.querySelector(s);
            if(el) {{
                let tracker = el._valueTracker;
                if(tracker) tracker.setValue('');
                el.value = v;
                el.dispatchEvent(new Event('input', {bubbles: true}));
                el.dispatchEvent(new Event('change', {bubbles: true}));
            }}
        }}''', input_selector, submit_value)
        await page.fill(input_selector, submit_value, force=True)
    except Exception:
        pass

    if submit_btn:
        try:
            await page.click(submit_btn, force=True)
        except Exception:
            pass
