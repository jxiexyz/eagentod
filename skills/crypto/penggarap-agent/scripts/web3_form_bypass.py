# Metadata: Domain: inkquills.xyz, Date: 2026-08-24, Symptom: React synthetic events dropping Playwright fill interactions and OAuth popups hanging main thread

async def react_fill(page, selector: str, value: str):
    """Fills an input bypassing React's event swallowing by dispatching native DOM events."""
    await page.wait_for_selector(selector, state='attached')
    await page.evaluate('''([sel, val]) => {
        const el = document.querySelector(sel);
        const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeInputValueSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
    }''', [selector, value])

async def handle_oauth_popup(page, trigger_selector: str):
    """Clicks an OAuth button (e.g., Follow/Repost on X) and automatically handles the resulting popup window."""
    async with page.expect_popup() as popup_info:
        await page.click(trigger_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    # Auto-click authorize if X/Twitter consent button exists
    auth_btn = popup.locator('button[data-testid="OAuth_Consent_Button"]')
    if await auth_btn.count() > 0:
        await auth_btn.click()
        
    # Wait for the popup to complete its redirect and close
    await popup.wait_for_event('close', timeout=15000)
