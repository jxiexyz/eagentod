# Metadata: Domain: form.typeform.com | Date: 2026-08-24 | Symptom: Standard Playwright click/fill fails on custom Typeform React SPA; requires keyboard-driven navigation.

import asyncio
from playwright.async_api import Page

async def bypass_typeform_step(page: Page, input_text: str = None, choice_key: str = None, advance_key: str = 'Enter', animation_delay: int = 1500):
    """
    Bypass for Typeform UI using global keyboard events instead of rigid DOM selectors.
    Handles text inputs, multiple choice (A, B, C), and advancing slides.
    """
    # Wait for Typeform slide transition animation
    await page.wait_for_timeout(animation_delay)
    
    if input_text:
        await page.keyboard.type(input_text, delay=50)
        await page.wait_for_timeout(500)
    elif choice_key:
        await page.keyboard.press(choice_key.upper())
        await page.wait_for_timeout(500)
        
    # Advance to next slide
    await page.keyboard.press(advance_key)
    await page.wait_for_timeout(animation_delay)
    return True