# Metadata: Domain: Generic (e.g., bubblebuns.xyz), Date: 2026-08-27, Symptom: Playwright fails to fill or submit React-based WL wallet forms due to event listener obfuscation or missing basic HTML attributes.

async def force_submit_form(page, input_data: str, input_selector: str = "input[type='text'], input[placeholder*='address' i]", submit_selector: str = "button"): 
    '''Forces typing into obfuscated React inputs to trigger onChange events and submits.'''
    inputs = await page.locator(input_selector).all()
    for el in inputs:
        if await el.is_visible():
            await el.click(force=True)
            await el.evaluate("node => node.value = ''")
            await el.type(input_data, delay=50)
            break
            
    submits = await page.locator(submit_selector).all()
    for btn in submits:
        if await btn.is_visible() and not await btn.is_disabled():
            btn_text = await btn.text_content()
            if btn_text and any(keyword in btn_text.lower() for keyword in ['submit', 'join', 'verify', 'confirm', 'save']):
                await btn.click(force=True)
                return True
                
    await page.keyboard.press("Enter")
    return True
