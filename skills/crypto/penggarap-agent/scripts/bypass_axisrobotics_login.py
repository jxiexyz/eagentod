# Metadata: hub.axisrobotics.ai, 2026-08-22, Invite Code Login Bypass
import asyncio
from playwright.async_api import Page, TimeoutError

async def run(page: Page, invite_code: str, **kwargs):
    """Generic bypass for SPA invite code login walls."""
    try:
        await page.wait_for_load_state('networkidle', timeout=10000)
    except TimeoutError:
        pass

    # Fallback heuristic selectors for invite code
    selectors = [
        "input[name*='invite' i]",
        "input[placeholder*='invite' i]",
        "input[placeholder*='code' i]",
        "input[type='text']"
    ]
    
    input_element = None
    for selector in selectors:
        try:
            elem = await page.wait_for_selector(selector, state="visible", timeout=3000)
            if elem:
                input_element = elem
                break
        except TimeoutError:
            continue

    if input_element:
        await input_element.fill(invite_code)
        await asyncio.sleep(1) # Humanize interaction

    # Fallback heuristic selectors for submit button
    btn_selectors = [
        "button[type='submit']",
        "button:has-text('Submit')",
        "button:has-text('Login')",
        "button:has-text('Enter')",
        "button:has-text('Join')",
        "button"
    ]
    
    for btn_sel in btn_selectors:
        try:
            btn = await page.wait_for_selector(btn_sel, state="visible", timeout=3000)
            if btn:
                await btn.click()
                break
        except TimeoutError:
            continue
            
    try:
        await page.wait_for_load_state('networkidle', timeout=10000)
    except TimeoutError:
        pass
        
    return True
