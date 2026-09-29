# Metadata: Origin: playwithmimo.xyz, Date: 2026-08-22, Symptom: Waitlist email form submission failure (React/Synthetic event blockers)
import asyncio

async def bypass_waitlist_form(page, email: str, email_selector: str = 'input[type="email"]', submit_selector: str = 'button[type="submit"]', fallback_enter: bool = True):
    """
    Bypasses standard React event blockers for waitlist forms by simulating real typing and click events.
    """
    email_input = await page.wait_for_selector(email_selector, state='visible', timeout=10000)
    if not email_input:
        raise Exception(f"Could not find email input using selector: {email_selector}")

    # Simulate realistic typing to trigger React onChange
    await email_input.click()
    await email_input.fill("")
    await email_input.type(email, delay=100)
    
    try:
        submit_btn = await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
        if submit_btn:
             await submit_btn.wait_for_element_state('enabled', timeout=3000)
             await submit_btn.click()
    except Exception:
        if fallback_enter:
             await email_input.press('Enter')
        else:
             raise
    
    # Allow time for network response/DOM update
    await page.wait_for_timeout(3000)
    return True
