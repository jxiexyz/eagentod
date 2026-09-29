# Metadata: Domain: memebitcoin.org, Date: 2026-08-24, Symptom: Social account connection failure and React form input drops

import asyncio

async def react_fill(page, selector: str, value: str):
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) return;
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def handle_oauth_popup(context, page, button_selector: str):
    async with context.expect_page() as popup_info:
        await page.locator(button_selector).click()
    popup = await popup_info.value
    await popup.wait_for_load_state('networkidle')
    return popup
