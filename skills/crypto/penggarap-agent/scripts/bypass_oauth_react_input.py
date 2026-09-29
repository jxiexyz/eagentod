# Metadata: Origin Domain: robinex.app, Date: 2026-08-23, Symptom: Fails to capture X OAuth popup and input Solana address in React form.

async def bypass_oauth_and_react_input(page, oauth_trigger_selector, input_selector, input_value, submit_selector=None):
    async with page.context.expect_page() as popup_info:
        await page.locator(oauth_trigger_selector).click()
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    
    auth_btn = popup.locator("button:has-text('Authorize app'), [data-testid='OAuth_Consent_Button']")
    if await auth_btn.is_visible(timeout=10000):
        await auth_btn.click()
    
    try:
        await popup.wait_for_event('close', timeout=15000)
    except:
        pass
    
    await page.wait_for_selector(input_selector, state='visible')
    await page.evaluate('''([selector, val]) => {
        const el = document.querySelector(selector);
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        nativeSetter.call(el, val);
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    }''', [input_selector, input_value])
    
    if submit_selector:
        await page.locator(submit_selector).click()
        await page.wait_for_load_state('networkidle')