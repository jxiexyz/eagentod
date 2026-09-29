# Origin Domain: sexyhood.xyz
# Date: 2026-09-01
# Symptom: React/SPA inputs swallow standard .fill() for X username and EVM address.

async def fill_react_input(page, selector: str, value: str):
    element = page.locator(selector).first
    await element.scroll_into_view_if_needed()
    await element.click()
    await element.evaluate('(el) => el.value = ""')
    await element.press_sequentially(value, delay=35)
    
    await page.evaluate('''(sel) => {
        const el = document.querySelector(sel);
        if (el) {
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            el.dispatchEvent(new Event('blur', { bubbles: true }));
        }
    }''', selector)
    
    return True
