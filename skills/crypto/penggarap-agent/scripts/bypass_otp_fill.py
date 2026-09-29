# Metadata: Origin: intersticedigital.io | Date: 2026-08-21 | Symptom: Web automation fails to fill OTP in split-input or strict validation forms
import asyncio
from playwright.async_api import Page

async def bypass_otp_fill(page: Page, otp_code: str, input_selector: str = 'input[type="text"]'):
    """
    Bypasses strict OTP fields by iterating through inputs or typing with human delays.
    """
    inputs = await page.locator(input_selector).all()
    if not inputs:
        return False
        
    if len(inputs) > 1:
        # Handle split OTP inputs (one digit per field)
        for i, char in enumerate(otp_code):
            if i < len(inputs):
                await inputs[i].focus()
                await page.keyboard.type(char, delay=100)
    else:
        # Handle single strict input
        await inputs[0].focus()
        await inputs[0].clear()
        await page.keyboard.type(otp_code, delay=100)
        
    await page.wait_for_timeout(500)
    return True
