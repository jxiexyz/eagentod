# Metadata: Origin Domain: rewards.svpstars.com, Date: 2026-09-22, Symptom: Automated quiz form submission failure / React state not triggering
import asyncio

async def fill_react_quiz(page, answers: list, submit_selector: str = 'button[type="submit"]'):
    """
    Fills a sequence of inputs, simulating real typing to trigger React/Vue state updates.
    """
    await page.wait_for_selector('input, textarea', timeout=10000)
    
    elements = await page.evaluate_handle('''() => {
        return Array.from(document.querySelectorAll('input[type="text"], input:not([type]), textarea'))
            .filter(el => el.offsetParent !== null && !el.disabled);
    }''')
    
    count = await page.evaluate('(els) => els.length', elements)
    
    for i, answer in enumerate(answers):
        if i < count:
            await page.evaluate('(els, idx) => els[idx].focus()', elements, i)
            await page.keyboard.type(str(answer), delay=50)
            await asyncio.sleep(0.5)
            
    try:
        submit_btn = await page.wait_for_selector(submit_selector, timeout=3000)
        if submit_btn:
            await submit_btn.click()
            await asyncio.sleep(2)
    except Exception:
        pass
        
    return True
