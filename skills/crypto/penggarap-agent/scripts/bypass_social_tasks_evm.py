# Metadata: Origin Domain: hub.axisrobotics.ai, Date: 2026-08-22, Symptom: Cannot fill EVM address or complete social login due to React/popup blocks
import asyncio

async def force_fill_input(page, selector: str, value: str):
    """Force fill React inputs bypassing synthetic events."""
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        if (!el) throw new Error("Selector not found: " + sel);
        const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [selector, value])

async def handle_oauth_popup(page, trigger_selector: str, auth_button_selector: str = 'button:has-text("Authorize")'):
    """Handle external OAuth popups (X/Discord)."""
    async with page.expect_popup() as popup_info:
        await page.locator(trigger_selector).click()
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    try:
        if await popup.locator(auth_button_selector).is_visible(timeout=5000):
            await popup.locator(auth_button_selector).click()
        await popup.wait_for_event('close', timeout=15000)
    except Exception as e:
        print(f"Popup handling error or auto-closed: {e}")