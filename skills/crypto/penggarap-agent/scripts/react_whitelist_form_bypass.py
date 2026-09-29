# Metadata: Origin: inkpunk.xyz, Date: 2026-08-25, Symptom: React synthetic input block and social tab hangs
import asyncio
from playwright.async_api import Page

async def bypass_social_and_submit(page: Page, input_selector: str, address: str, social_selectors: list, submit_selector: str):
    # Prevent new tabs from blocking Playwright context
    await page.evaluate("() => { window.open = () => null; document.querySelectorAll('a[target=\"_blank\"]').forEach(el => el.removeAttribute('target')); }")
    
    for selector in social_selectors:
        element = await page.query_selector(selector)
        if element:
            await element.click()
            await page.wait_for_timeout(1000)
            
    input_el = await page.wait_for_selector(input_selector)
    await input_el.focus()
    await page.keyboard.type(address, delay=50)
    
    # Bypass React synthetic event ignoring native input
    await page.evaluate(f"""(sel) => {{
        let node = document.querySelector(sel);
        if (node) {{
            let tracker = node._valueTracker;
            if (tracker) tracker.setValue('');
            node.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    }}""", input_selector)
    
    submit_btn = await page.wait_for_selector(submit_selector)
    if submit_btn:
        await submit_btn.click()
