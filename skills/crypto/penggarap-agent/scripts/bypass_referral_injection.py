# Metadata: Origin: register.divvy.bet, Date: 2026-08-24, Symptom: Referral code input hidden or requires forced event dispatch
import asyncio

async def inject_referral_code(page, toggle_selector: str, input_selector: str, code: str):
    """Clicks an optional toggle if present, then forcefully injects a promo/referral code bypassing SPA event traps."""
    try:
        toggle = page.locator(toggle_selector)
        if await toggle.is_visible(timeout=3000):
            await toggle.click()
    except Exception:
        pass
    
    inp = page.locator(input_selector)
    await inp.wait_for(state="attached", timeout=5000)
    await inp.fill(code)
    
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (el) {
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
            if (nativeSetter) nativeSetter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }""", [input_selector, code])
