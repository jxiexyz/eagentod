# Origin Domain: tally.so (Generic React SPA Forms)
# Date: 2026-08-24
# Specific Symptom: React synthetic event blocking, multi-step animation delays, click interception.

async def fill_and_advance(page, step_configs: list):
    """
    Iterates through form steps for React-based forms with animations.
    page: Playwright page object
    step_configs: list of dicts [{'input': selector, 'value': str, 'next_btn': selector}]
    """
    for step in step_configs:
        if 'input' in step and step['value']:
            field = page.locator(step['input']).first
            await field.wait_for(state="attached", timeout=15000)
            await field.scroll_into_view_if_needed()
            await field.fill(step['value'])
            # Trigger React state update
            await field.press('Tab')
        
        if 'next_btn' in step and step.get('next_btn'):
            btn = page.locator(step['next_btn']).first
            await btn.wait_for(state="attached", timeout=5000)
            await btn.click(force=True)
            # Wait for slide/fade animations between steps
            await page.wait_for_timeout(1500)
