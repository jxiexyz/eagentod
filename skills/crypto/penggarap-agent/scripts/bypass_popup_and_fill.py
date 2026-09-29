# Metadata: Origin Domain: octra.fun, Date: 2026-08-26, Symptom: Playwright hangs on external protocol links (tg://) or social popups during task completion.
import asyncio
from playwright.async_api import Page, Route

async def bypass_popup_and_fill(page: Page, action_selector: str = None, input_selector: str = None, input_value: str = None, submit_selector: str = None):
    """
    Intercepts external app prompts, handles social popup windows safely, and submits form data.
    """
    async def handle_route(route: Route):
        if route.request.url.startswith(('tg:', 'intent:', 'twitter:')):
            await route.abort()
        else:
            await route.continue_()
            
    await page.route('**/*', handle_route)
    
    try:
        if action_selector:
            try:
                async with page.expect_event('popup', timeout=3000) as popup_info:
                    await page.locator(action_selector).click(force=True)
                popup = await popup_info.value
                await popup.close()
            except Exception:
                pass
                
        if input_selector and input_value:
            await page.locator(input_selector).wait_for(state='visible', timeout=5000)
            await page.locator(input_selector).fill(input_value)
            
        if submit_selector:
            await page.locator(submit_selector).click(force=True)
            try:
                await page.wait_for_load_state('networkidle', timeout=3000)
            except Exception:
                pass
                
        return True
    finally:
        await page.unroute('**/*', handle_route)