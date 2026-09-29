# Metadata: mudlarknft.com, 2026-08-21, Waitlist form requiring sequential quest button clicks before submission
import asyncio

async def bypass(page, quest_selector, inputs_map, submit_selector, success_text):
    """
    Generic bypass for waitlist forms that require clicking quest buttons first,
    filling text inputs, and then submitting.
    
    quest_selector: CSS selector for quest buttons to bypass (e.g., '.quest')
    inputs_map: Dictionary mapping selectors to values (e.g., {'#username': 'foo'})
    submit_selector: CSS selector for the final submit button
    success_text: Substring to verify successful submission in page text
    """
    if quest_selector:
        await page.evaluate(f'''(selector) => {{
            const btns = document.querySelectorAll(selector);
            btns.forEach(btn => btn.click());
        }}''', quest_selector)
        await asyncio.sleep(2)
        
    for selector, value in inputs_map.items():
        await page.fill(selector, value)
        
    await asyncio.sleep(1)
    
    if submit_selector:
        await page.click(submit_selector)
        await asyncio.sleep(4)
        
    if success_text:
        result_text = await page.evaluate('document.body.innerText')
        if success_text in result_text:
            return True
        else:
            raise Exception(f"Success artifact '{success_text}' not found in DOM.")
            
    return True