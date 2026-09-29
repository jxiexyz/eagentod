# Origin Domain: Generic (Context: nft-relics.xyz)
# Date: 2026-08-26
# Specific Symptom: React SPA ignores standard Playwright page.fill(), leaving EVM address fields empty.

async def bypass_react_input(page, selector: str, value: str):
    """Force input value by bypassing React synthetic events."""
    element = await page.wait_for_selector(selector, state='attached')
    if element:
        await page.evaluate('''([el, val]) => {
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeSetter.call(el, val);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }''', [element, value])

async def submit_waitlist_form(page, address: str, input_selector: str = 'input', submit_selector: str = 'button'):
    """Finds and fills EVM waitlist form using React bypass."""
    inputs = await page.locator(input_selector).all()
    for el in inputs:
        placeholder = (await el.get_attribute('placeholder') or '').lower()
        name = (await el.get_attribute('name') or '').lower()
        if '0x' in placeholder or 'address' in placeholder or 'wallet' in name:
            await bypass_react_input(page, input_selector, address)
            break

    buttons = await page.locator(submit_selector).all()
    for btn in buttons:
        text = (await btn.inner_text()).lower()
        if any(kw in text for kw in ['submit', 'join', 'register', 'waitlist', 'enter']):
            await btn.click()
            break
