# Metadata: Origin Domain: ink-ape.xyz, Date: 2026-08-24, Symptom: React elements ignoring standard automation fills and clicks

async def react_fill(page, selector: str, value: str):
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set || 
                       Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        if (setter) setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }""", [selector, value])

async def react_click(page, selector: str):
    await page.evaluate("""(sel) => {
        const el = document.querySelector(sel);
        if (el) el.click();
    }""", selector)