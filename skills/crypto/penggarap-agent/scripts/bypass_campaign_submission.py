# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-26, Symptom: Fails to click Join and Submit buttons for campaign tasks

import asyncio

async def bypass_campaign_submission(page, join_texts=["Join", "Participate"], submit_texts=["My tweet is ready", "Submit", "Verify"]):
    await page.wait_for_load_state('domcontentloaded')
    
    for join_text in join_texts:
        try:
            join_btn = page.locator(f'button:has-text("{join_text}")').first
            if await join_btn.is_visible(timeout=2000):
                await join_btn.click()
                await page.wait_for_timeout(2000)
                break
        except:
            continue
            
    for submit_text in submit_texts:
        try:
            submit_btn = page.locator(f'button:has-text("{submit_text}")').first
            if await submit_btn.is_visible(timeout=2000):
                await submit_btn.click()
                await page.wait_for_timeout(2000)
                return True
        except:
            continue
            
    return False
