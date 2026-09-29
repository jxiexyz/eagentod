# Metadata: Domain: digitsbt.ngrndrewards.com, Date: 2026-08-24, Symptom: SPA ignores standard Playwright inputs (React/Vue synthetic events)
import asyncio

async def robust_fill(page, selector: str, value: str):
    element = await page.wait_for_selector(selector, state='visible', timeout=10000)
    await element.click()
    await page.keyboard.press('Control+A')
    await page.keyboard.press('Backspace')
    await element.type(value, delay=75)
    await page.evaluate('''(sel) => {
        const el = document.querySelector(sel);
        if(el) {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
        }
    }''', selector)
    await asyncio.sleep(0.5)

async def robust_click(page, selector: str):
    try:
        await page.click(selector, timeout=3000)
    except Exception:
        await page.evaluate('(sel) => document.querySelector(sel)?.click()', selector)
    await asyncio.sleep(0.5)