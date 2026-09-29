# Origin Domain: inklords.xyz
# Date: 2026-08-25
# Specific Symptom: React inputs ignoring Playwright .fill() and social tasks hanging on new tabs.

async def force_react_fill(page, selector: str, value: str):
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const proto = el.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        if (setter) setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def trigger_social_task(page, selector: str):
    try:
        async with page.context.expect_page(timeout=5000) as new_page_info:
            await page.click(selector)
        new_page = await new_page_info.value
        await new_page.close()
    except Exception:
        pass
