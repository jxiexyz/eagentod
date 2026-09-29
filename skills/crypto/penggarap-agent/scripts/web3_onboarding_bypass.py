# Metadata: Origin Domain: event.neosoul.ai, Date: 2026-08-21, Symptom: Web3 wallet connection, invite code injection, and Twitter OAuth popup blocked by React synthetic events and shadow overlays.

import asyncio

async def bypass_web3_onboarding(page, invite_code_selector: str = None, invite_code: str = None, wallet_btn_selector: str = None):
    """Generic Web3 onboarding bypass for React/Shadow DOM & popups."""
    # 1. Bypass React synthetic event blockers for input values
    if invite_code_selector and invite_code:
        await page.wait_for_selector(invite_code_selector, state="attached", timeout=10000)
        await page.evaluate(f'''(selector, val) => {{
            const el = document.querySelector(selector);
            if (el) {{
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
                nativeInputValueSetter.call(el, val);
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}''', invite_code_selector, invite_code)
        
    # 2. Force click elements (bypasses z-index overlays)
    if wallet_btn_selector:
        await page.wait_for_selector(wallet_btn_selector, state="attached", timeout=5000)
        await page.evaluate(f'''(sel) => {{
            const el = document.querySelector(sel) || document.evaluate(sel, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            if (el) el.click();
        }}''', wallet_btn_selector)

    # 3. Auto-handle typical Twitter OAuth popup authorization
    page.on("popup", lambda popup: asyncio.create_task(_handle_oauth_popup(popup)))

async def _handle_oauth_popup(popup):
    try:
        await popup.wait_for_load_state("domcontentloaded")
        if "twitter.com" in popup.url or "x.com" in popup.url:
            allow_btn = await popup.wait_for_selector('[data-testid="OAuth_Consent_Button"]', timeout=15000)
            if allow_btn:
                await allow_btn.click()
    except Exception:
        pass
