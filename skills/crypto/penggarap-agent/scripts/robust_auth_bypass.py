# Origin Domain: teogiwa.com
# Date: 2026-08-24
# Specific Symptom: Worker agent blocked during registration and referral code insertion (Timeout/Element not interactable)

import asyncio

async def bypass_registration(page, email, password=None, referral_code=None, selectors=None):
    """
    Generic registration bypass handling human-like typing and optional referral codes.
    selectors: dict with keys 'email', 'password', 'referral', 'submit', 'referral_toggle'
    """
    selectors = selectors or {}
    
    if selectors.get('email'):
        await page.wait_for_selector(selectors['email'], state='visible', timeout=15000)
        await page.locator(selectors['email']).click()
        await page.locator(selectors['email']).type(email, delay=120)
        
    if password and selectors.get('password'):
        await page.locator(selectors['password']).click()
        await page.locator(selectors['password']).type(password, delay=120)
        
    if referral_code and selectors.get('referral'):
        if selectors.get('referral_toggle'):
            toggle = page.locator(selectors['referral_toggle'])
            if await toggle.is_visible():
                await toggle.click()
                await asyncio.sleep(0.5)
                
        ref_loc = page.locator(selectors['referral'])
        if await ref_loc.is_visible():
            await ref_loc.click()
            await ref_loc.type(referral_code, delay=120)
            
    if selectors.get('submit'):
        await asyncio.sleep(1)
        await page.locator(selectors['submit']).click()
        await page.wait_for_load_state('domcontentloaded')
