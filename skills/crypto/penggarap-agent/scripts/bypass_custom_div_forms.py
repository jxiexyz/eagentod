# Metadata: forms.gle, 2026-08-22, Symptom: Standard page.fill fails on custom DIV-based inputs
import asyncio

async def fill_custom_div_form(page, questions_answers: dict):
    """
    Fills DIV-based forms (e.g. Google Forms) where standard inputs are hidden.
    """
    for q, a in questions_answers.items():
        # Scope to the question container
        q_loc = page.locator(f'text="{q}"').locator('xpath=ancestor::div[1]')
        
        # 1. Text inputs
        text_in = q_loc.locator('input[type="text"], input[type="url"], textarea').first
        if await text_in.is_visible():
            await text_in.fill(str(a))
            continue
        
        # 2. Radio/Checkboxes
        opt_in = q_loc.locator(f'div[role="radio"], div[role="checkbox"]').filter(has_text=str(a)).first
        if await opt_in.is_visible():
            await opt_in.click()
            continue
            
        # 3. Fallback generic input
        fallback = q_loc.locator('input:not([type="hidden"])').first
        if await fallback.is_visible():
            await fallback.fill(str(a))
