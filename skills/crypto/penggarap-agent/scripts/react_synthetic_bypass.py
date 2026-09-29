# Metadata: Origin Domain: nft.retium.org, Date: 2026-08-22, Symptom: Playwright fill/click intercepted or ignored by React synthetic events during EVM address submission.

async def react_fill_and_force_click(page, input_selector: str, value: str, submit_selector: str = None):
    """
    Bypass React synthetic events and overlapping overlays to fill inputs and click submit.
    """
    await page.evaluate('''([in_sel, val]) => {
        const el = document.querySelector(in_sel);
        if (!el) return;
        let proto = window.HTMLInputElement.prototype;
        if (el.tagName && el.tagName.toLowerCase() === 'textarea') {
            proto = window.HTMLTextAreaElement.prototype;
        }
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        if (nativeSetter) {
            nativeSetter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }''', [input_selector, value])

    if submit_selector:
        await page.evaluate('''([sub_sel]) => {
            const btn = document.querySelector(sub_sel);
            if (btn) btn.click();
        }''', [submit_selector])
