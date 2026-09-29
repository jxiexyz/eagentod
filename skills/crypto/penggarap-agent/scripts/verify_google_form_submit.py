# Origin Domain: docs.google.com
# Date: 2026-08-18
# Symptom: Worker claimed success but provided NO valid VERIFICATION artifact on form submit.

async def verify_google_form_submit(page):
    submit_selectors = [
        'div[role="button"]:has-text("Submit")',
        'span:text-is("Submit")',
        'div[role="button"]:has-text("Kirim")'
    ]
    for sel in submit_selectors:
        try:
            btn = page.locator(sel).first
            if await btn.is_visible(timeout=2000):
                await btn.click()
                break
        except Exception:
            pass

    try:
        await page.wait_for_load_state("networkidle", timeout=5000)
    except Exception:
        pass

    confirmation_selectors = [
        '.freebirdFormviewerViewResponseConfirmationMessage',
        'div.vHW8K',
        'div[role="heading"]:has-text("recorded")',
        'div[role="heading"]:has-text("terekam")'
    ]
    for sel in confirmation_selectors:
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=3000):
                return await el.inner_text()
        except Exception:
            pass

    try:
        body_text = await page.locator("body").inner_text()
        if "recorded" in body_text.lower() or "terekam" in body_text.lower():
            return "Form submitted successfully (text matched in body)."
    except Exception:
        pass

    raise Exception("Failed to find Google Form submission verification artifact.")
