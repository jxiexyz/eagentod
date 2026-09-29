# Metadata: Domain: puffins.fun, Date: 2026-08-22, Symptom: t.me redirects hang the VPS worker / React wallet inputs ignore typing

async def bypass_tg_and_submit_wallet(page, wallet_address: str):
    """
    Prevents t.me redirects from hanging the browser, extracts the bot link,
    and natively injects the wallet address into React-controlled inputs.
    """
    bot_links = []
    
    # 1. Intercept t.me redirects to prevent VPS hang
    async def intercept_tg(route):
        if 't.me' in route.request.url:
            bot_links.append(route.request.url)
            await route.abort()
        else:
            await route.continue_()
    
    await page.route("**/*", intercept_tg)
    
    # 2. Extract TG links directly from DOM
    tg_elements = page.locator("a[href*='t.me']")
    for i in range(await tg_elements.count()):
        href = await tg_elements.nth(i).get_attribute("href")
        if href:
            bot_links.append(href)
        
    # 3. Bypass React synthetic events for wallet submission
    input_sel = "input[placeholder*='0x'], input[placeholder*='BSC' i], input[placeholder*='Address' i]"
    inputs = page.locator(input_sel)
    
    wallet_submitted = False
    if await inputs.count() > 0:
        await inputs.first.evaluate(
            "(el, val) => { "
            "const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set; "
            "setter.call(el, val); "
            "el.dispatchEvent(new Event('input', { bubbles: true })); "
            "el.dispatchEvent(new Event('change', { bubbles: true })); "
            "}", wallet_address
        )
        
        submit_sel = "button:has-text('Submit'), button:has-text('Confirm'), button:has-text('Save')"
        submit_btn = page.locator(submit_sel)
        if await submit_btn.count() > 0:
            await submit_btn.first.click()
        wallet_submitted = True
            
    return {
        "extracted_tg_links": list(set(bot_links)),
        "wallet_submitted": wallet_submitted
    }
