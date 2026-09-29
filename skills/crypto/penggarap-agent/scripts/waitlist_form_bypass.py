# Metadata: Domain: theinkylabs.xyz, Date: 2026-08-24, Symptom: Waitlist form interaction failure (hidden elements/shadow DOM)

async def bypass_waitlist(page, input_data, input_selectors=None, submit_selectors=None):
    """
    Aggressively locate and fill waitlist forms, piercing shadow DOMs if necessary.
    """
    if not input_selectors:
        input_selectors = [
            'input[type="email"]', 
            'input[name*="email" i]', 
            'input[placeholder*="email" i]',
            'input[name*="wallet" i]',
            'input[placeholder*="address" i]'
        ]
    if not submit_selectors:
        submit_selectors = [
            'button[type="submit"]', 
            'button:has-text("Join")', 
            'button:has-text("Apply")', 
            'button:has-text("Submit")',
            'div[role="button"]:has-text("Join")'
        ]

    filled = False
    for selector in input_selectors:
        elements = await page.locator(selector).all()
        for el in elements:
            if await el.is_visible():
                await el.fill(input_data)
                filled = True
                break
        if filled:
            break

    if not filled:
        return False

    for selector in submit_selectors:
        elements = await page.locator(selector).all()
        for el in elements:
            if await el.is_visible():
                await el.click()
                await page.wait_for_timeout(2000)
                return True
                
    return False
