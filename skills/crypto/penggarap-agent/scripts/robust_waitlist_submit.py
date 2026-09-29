# Metadata: Origin Domain: conso.xyz, Date: 2026-08-25, Symptom: Waitlist form submission failure (FCFS queue)
import asyncio

async def bypass(page, input_selector: str, button_selector: str, value: str):
    await page.wait_for_selector(input_selector, state='visible', timeout=15000)
    
    js_fill = """(selector, val) => {
        const input = document.querySelector(selector);
        if (!input) return;
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (nativeSetter) {
            nativeSetter.call(input, val);
        } else {
            input.value = val;
        }
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
    }"""
    
    await page.evaluate(js_fill, input_selector, value)
    await page.type(input_selector, " ")
    await page.keyboard.press("Backspace")
    
    await page.wait_for_selector(button_selector, state='attached', timeout=5000)
    js_click = """(selector) => {
        const btn = document.querySelector(selector);
        if (btn) btn.click();
    }"""
    await page.evaluate(js_click, button_selector)
    await asyncio.sleep(2)
    return True