# Metadata: Origin Domain: nft.retium.org | Date: 2026-08-20 | Symptom: Standard automation fails to input email and select country on waitlist forms due to React/synthetic event blocking and custom dropdown UIs.

import asyncio
from playwright.async_api import Page

async def fill_waitlist_form(page: Page, email: str, country: str = 'United States', email_selector: str = 'input[type="email"]', custom_country_selector: str = None, submit_selector: str = 'button[type="submit"]'):
    """Robustly fills email and selects country on standard or headless UI waitlist forms."""
    # 1. Fill email and force React state update
    await page.wait_for_selector(email_selector, state='visible', timeout=10000)
    await page.focus(email_selector)
    await page.fill(email_selector, '')
    await page.type(email_selector, email, delay=50)
    await page.evaluate(f"document.querySelector('{email_selector}').dispatchEvent(new Event('input', {{ bubbles: true }}))")
    await page.evaluate(f"document.querySelector('{email_selector}').dispatchEvent(new Event('change', {{ bubbles: true }}))")

    # 2. Select Country
    if custom_country_selector:
        # Custom UI Dropdown
        await page.click(custom_country_selector)
        await page.wait_for_timeout(500)
        await page.get_by_text(country).first.click()
    else:
        # Try standard select first
        selects = await page.locator('select').all()
        handled = False
        for select in selects:
            try:
                await select.select_option(label=country, timeout=1000)
                handled = True
                break
            except Exception:
                continue
        
        if not handled:
            # Try guessing standard headless UI country selector
            dropdown = page.locator('text=/Country/i, text=/Select/i').locator('xpath=..').first
            if await dropdown.is_visible():
                await dropdown.click()
                await page.wait_for_timeout(500)
                await page.get_by_text(country).first.click()

    # 3. Submit Form
    await page.wait_for_timeout(500)
    submit_btn = page.locator(submit_selector)
    if not await submit_btn.is_visible():
        submit_btn = page.locator('button', has_text='Join').first
        if not await submit_btn.is_visible():
            submit_btn = page.locator('button', has_text='Submit').first
            
    await submit_btn.click()
    try:
        await page.wait_for_load_state('networkidle', timeout=5000)
    except Exception:
        pass # Ignore networkidle timeout if submission succeeded but page remains busy
