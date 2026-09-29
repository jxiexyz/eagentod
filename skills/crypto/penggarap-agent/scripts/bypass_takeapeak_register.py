# Metadata: Domain: takeapeak.ai, Date: 2026-08-25, Symptom: Worker unable to register and follow account (session_id: 20260825_050440_17e495)

import asyncio
import logging

logger = logging.getLogger(__name__)

async def run(page, target_account="NoosProtocol"):
    logger.info(f"Starting takeapeak.ai register & follow bypass for {target_account}")
    try:
        await page.wait_for_load_state('domcontentloaded', timeout=15000)
    except Exception:
        pass

    login_selectors = [
        "button:has-text('Connect')", 
        "button:has-text('Login')", 
        "button:has-text('Register')", 
        "button:has-text('Sign In')"
    ]
    for sel in login_selectors:
        btn = page.locator(sel).first
        if await btn.is_visible():
            await btn.click()
            await asyncio.sleep(3)
            break

    follow_selectors = [
        f"button:has-text('Follow {target_account}')", 
        "button:has-text('Follow')"
    ]
    for _ in range(5):
        for sel in follow_selectors:
            btn = page.locator(sel).first
            if await btn.is_visible():
                await btn.click()
                logger.info("Follow clicked.")
                await asyncio.sleep(2)
                return True
        await asyncio.sleep(2)
    
    logger.warning("Follow button not found.")
    return False
