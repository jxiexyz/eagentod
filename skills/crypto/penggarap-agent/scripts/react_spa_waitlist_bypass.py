# Metadata: Domain: conso.xyz, Date: 2026-08-25, Symptom: Waitlist button unclickable / React hydration blocking form submission
import asyncio
from playwright.async_api import Page

async def bypass_react_waitlist(page: Page, input_selector: str, input_value: str, submit_selector: str):
    await page.wait_for_selector(input_selector, state="attached", timeout=10000)
    
    # Strip disabled constraints via JS
    await page.evaluate('''([inSel, subSel]) => {
        const inputs = document.querySelectorAll(inSel);
        inputs.forEach(el => { el.removeAttribute('disabled'); el.removeAttribute('readonly'); });
        const buttons = document.querySelectorAll(subSel);
        buttons.forEach(el => { el.removeAttribute('disabled'); el.removeAttribute('aria-disabled'); });
    }''', [input_selector, submit_selector])
    
    input_loc = page.locator(input_selector).first
    await input_loc.focus()
    await input_loc.fill(input_value, force=True)
    
    # Dispatch native React change tracker events to trigger internal state updates
    await page.evaluate('''(sel) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const tracker = el._valueTracker;
        if (tracker) tracker.setValue('');
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', input_selector)
    
    submit_loc = page.locator(submit_selector).first
    await submit_loc.click(force=True)
    await asyncio.sleep(2)
    return True
