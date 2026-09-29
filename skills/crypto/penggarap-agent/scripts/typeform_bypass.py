# Metadata: Domain: typeform.com, Date: 2026-08-24, Symptom: Multi-step form automation failures due to UI transitions and hidden elements.
import asyncio
from playwright.async_api import Page

async def fill_multi_step_form(page: Page, answers: list, submit_btn_selector: str = 'button[data-qa="submit-button"]'):
    """
    Fills a Typeform or similar multi-step form utilizing keyboard navigation to bypass DOM transition blocks.
    answers: list of strings (text to type) or dicts ({'type': 'choice', 'value': 'A'}) for multiple choice.
    """
    await page.wait_for_load_state('networkidle')
    await page.wait_for_timeout(2000) # Wait for initial start screen/transition
    
    # Handle initial "Start" button if present (often mapped to Enter)
    await page.keyboard.press('Enter')
    await page.wait_for_timeout(1000)
    
    for answer in answers:
        if isinstance(answer, str):
            # Target the active visible input
            input_locator = page.locator('input:visible, textarea:visible').first
            if await input_locator.count() > 0:
                await input_locator.fill(answer)
            else:
                # Fallback to direct keyboard typing if inputs are shadow/hidden
                await page.keyboard.type(answer)
            await page.keyboard.press('Enter')
        elif isinstance(answer, dict) and answer.get('type') == 'choice':
            val = answer.get('value')
            await page.keyboard.press(val)
            await page.wait_for_timeout(500)
            await page.keyboard.press('Enter')
        
        # Wait for the next question to slide into the viewport
        await page.wait_for_timeout(1200)
        
    submit_btn = page.locator(submit_btn_selector)
    if await submit_btn.is_visible():
        await submit_btn.click()
    else:
        await page.keyboard.press('Enter')
    
    await page.wait_for_timeout(2000)
