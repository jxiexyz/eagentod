# Metadata: Origin Domain: rewards.svpstars.com, Date: 2026-09-27, Symptom: Playwright fill fails on SPA quiz inputs
import asyncio

async def bypass_react_inputs(page, selector_answer_map):
    """
    Bypass React/Vue synthetic events by setting native value and dispatching Event.
    selector_answer_map: dict of { css_selector: answer_text }
    """
    for selector, text in selector_answer_map.items():
        await page.wait_for_selector(selector, state="visible")
        await page.evaluate('''([sel, val]) => {
            const el = document.querySelector(sel);
            if (!el) return;
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value");
            const nativeTextAreaValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value");
            
            if (el.tagName.toUpperCase() === 'TEXTAREA' && nativeTextAreaValueSetter) {
                nativeTextAreaValueSetter.set.call(el, val);
            } else if (nativeInputValueSetter) {
                nativeInputValueSetter.set.call(el, val);
            } else {
                el.value = val;
            }
            
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }''', [selector, text])
        await asyncio.sleep(0.5)
