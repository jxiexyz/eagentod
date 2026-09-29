# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-29, Symptom: Failing to automate multi-step sequential quiz
import asyncio

async def execute_quiz_sequence(page, answers: list, next_btn_selector: str = "button:has-text('Next'), button:has-text('Submit'), button:has-text('Continue')"):
    """
    Iterates through a list of quiz answers, clicking each and proceeding.
    answers: list of strings (e.g., ['B', 'B', 'C', 'B', 'B', 'C', 'C'])
    """
    for ans in answers:
        # Locate option by text (e.g., 'A', 'B', 'C' or specific answer text)
        option = page.locator(f"text='{ans}'").first
        await option.wait_for(state="visible", timeout=10000)
        await option.click()
        
        await page.wait_for_timeout(500) # Give UI time to register selection
        
        # Locate and click the next/submit button if available
        next_btn = page.locator(next_btn_selector).first
        if await next_btn.is_visible():
            await next_btn.click()
            
        await page.wait_for_timeout(1500) # Wait for next question transition
        
    return True
