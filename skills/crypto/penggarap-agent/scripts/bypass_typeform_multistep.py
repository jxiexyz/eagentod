# Origin Domain: form.typeform.com
# Date: 2026-08-23
# Specific Symptom: Multi-step React form transitions failing standard page.fill() and requiring Enter keypresses or specific choice clicks
import asyncio

async def bypass_typeform(page, steps: list):
    """
    Navigates a Typeform multi-step presentation.
    steps: list of dicts, e.g. [{'type': 'text', 'val': '0x...'}, {'type': 'choice', 'val': 'Option A'}]
    """
    for step in steps:
        # Wait for Typeform slide transition animation to settle
        await asyncio.sleep(1.5)
        
        if step.get('type') == 'text':
            # Target the active input (Typeform uses opacity/visibility for off-screen slides)
            active_input = page.locator('input:not([type="hidden"]), textarea').first
            await active_input.fill(step['val'])
            await page.keyboard.press('Enter')
            
        elif step.get('type') == 'choice':
            # Locate the choice container containing the specific text
            choice = page.locator(f'div[role="button"]:has-text("{step["val"]}")').first
            await choice.click()
            
        else:
            # Fallback pure keyboard entry for generic prompts
            await page.keyboard.type(str(step['val']), delay=50)
            await page.keyboard.press('Enter')
