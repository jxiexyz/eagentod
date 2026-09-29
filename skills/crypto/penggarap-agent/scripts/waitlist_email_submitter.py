# Origin Domain: playwithmimo.xyz
# Date: 2026-08-22
# Symptom: Waitlist email input targeting and generic submission

async def bypass(page, email: str, input_selector: str = None, submit_selector: str = None):
    if not input_selector:
        for sel in ['input[type="email"]', 'input[name*="email" i]', 'input[placeholder*="email" i]']:
            if await page.locator(sel).count() > 0:
                input_selector = sel
                break
        if not input_selector:
            raise Exception("Email input not found.")

    await page.locator(input_selector).first.fill(email)

    if not submit_selector:
        for sel in ['button[type="submit"]', 'button:has-text("Join")', 'button:has-text("Submit")', 'button:has-text("Waitlist")']:
            if await page.locator(sel).count() > 0:
                submit_selector = sel
                break
        if not submit_selector:
            raise Exception("Submit button not found.")

    await page.locator(submit_selector).first.click()
    await page.wait_for_timeout(2000)
    return True