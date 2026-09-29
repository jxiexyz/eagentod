# Metadata: Domain: inkquills.xyz, Date: 2026-08-24, Symptom: Fails to handle X/Twitter OAuth or social task popups causing execution hangs.
import asyncio
from playwright.async_api import Page

async def handle_social_popup(page: Page, trigger_selector: str):
    """Clicks a social button, handles the resulting popup tab (OAuth/Intent), and returns control."""
    context = page.context
    async with context.expect_page() as popup_info:
        await page.click(trigger_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    if 'x.com/oauth' in popup.url or 'twitter.com/oauth' in popup.url:
        try:
            await popup.click('[data-testid="OAuth_Consent_Button"]', timeout=5000)
        except:
            pass # Already authorized or different UI state
            
    if 'intent/follow' in popup.url or 'intent/retweet' in popup.url:
        try:
            await popup.click('[data-testid="confirmationSheetConfirm"]', timeout=5000)
        except:
            pass

    try:
        await popup.wait_for_event('close', timeout=10000)
    except:
        if not popup.is_closed():
            await popup.close()
            
    await page.bring_to_front()
    return True

async def fill_evm_react(page: Page, address: str):
    """Force-fills EVM address bypassing React synthetic event blocks."""
    await page.evaluate(f"""(addr) => {{
        const input = document.querySelector('input[placeholder*="0x"], input[name*="address" i]');
        if(input) {{
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(input, addr);
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    }}""", address)