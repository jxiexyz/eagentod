# Metadata: Origin: playwithmimo.xyz | Date: 2026-08-22 | Symptom: General Waitlist Email Input Block/React Event Fail
import asyncio

async def bypass_email_waitlist(page, email: str, submit_text: str = None):
    """
    Generic waitlist email filler bypassing standard React/Vue synthetic event blockers.
    Locates heuristic email fields and dispatches native typing events.
    """
    selectors = [
        'input[type="email"]',
        'input[name="email"]',
        'input[placeholder*="email" i]',
        'input[placeholder*="Email" i]'
    ]
    
    email_input = None
    for sel in selectors:
        try:
            loc = page.locator(sel).first
            if await loc.is_visible(timeout=2000):
                email_input = loc
                break
        except Exception:
            continue
            
    if not email_input:
        raise Exception("Email input not found on page.")

    # React bypass: click and type natively instead of setting .value
    await email_input.scroll_into_view_if_needed()
    await email_input.click()
    # Clear existing if any
    await page.keyboard.press("Control+A")
    await page.keyboard.press("Backspace")
    await page.keyboard.type(email, delay=50)
    
    # Submit handling
    if submit_text:
        btn = page.locator(f'button:has-text("{submit_text}")').first
        if await btn.is_visible(timeout=1000):
            await btn.click()
            return True
            
    # Fallback heuristic submit
    submit_selectors = ['button[type="submit"]', 'button:has-text("Join")', 'button:has-text("Submit")']
    for s_sel in submit_selectors:
        try:
            btn = page.locator(s_sel).first
            if await btn.is_visible(timeout=1000):
                await btn.click()
                return True
        except:
            continue
            
    # Last resort: enter key
    await page.keyboard.press("Enter")
    return True
