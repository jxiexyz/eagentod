# Metadata: Origin Domain: fulelore.xyz, Date: 2026-08-21, Symptom: Element interception and React synthetic event blockers on whitelist forms
import asyncio

async def force_fill_and_submit(page, input_selector: str, value: str, submit_selector: str):
    try:
        await page.wait_for_load_state('domcontentloaded', timeout=10000)
    except Exception:
        pass
    
    # Bypass Playwright strict intersection checks and directly trigger React state updates
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (el) {
            el.value = val;
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }''', [input_selector, value])
    
    await asyncio.sleep(0.5)
    
    await page.evaluate('''([sel]) => {
        const btn = document.querySelector(sel);
        if (btn) btn.click();
    }''', [submit_selector])
    
    await asyncio.sleep(2)
    return True
