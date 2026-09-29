# Metadata: Origin Domain: commonsmade.com, Date: 2026-08-24, Symptom: Vouch code form submission failure
import re
import asyncio

async def bypass(page, code: str):
    await page.wait_for_load_state('domcontentloaded')
    
    input_loc = page.locator("input[placeholder*='code' i], input[name*='code' i], input[type='text']").first
    await input_loc.wait_for(state='visible', timeout=10000)
    await input_loc.fill(code)
    
    btn_loc = page.locator("button, input[type='submit']").filter(has_text=re.compile("(?i)redeem|claim|submit|vouch|apply|enter")).first
    
    if await btn_loc.count() > 0:
        await btn_loc.click()
    else:
        await page.keyboard.press('Enter')
        
    await page.wait_for_load_state('networkidle')
