# Metadata: Domain: Generic React Waitlist, Date: 2026-08-20, Symptom: Form inputs ignoring standard Playwright fill/type commands

async def inject_input(page, selector: str, value: str):
    await page.wait_for_selector(selector, timeout=10000)
    await page.evaluate("""([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        if (nativeInputValueSetter) {
            nativeInputValueSetter.call(el, val);
        } else {
            el.value = val;
        }
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }""", [selector, value])

async def force_click(page, selector: str):
    await page.wait_for_selector(selector, timeout=10000)
    await page.evaluate("""(sel) => {
        const el = document.querySelector(sel);
        if (el) {
            el.removeAttribute('disabled');
            el.click();
        }
    }""", selector)