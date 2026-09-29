# Metadata: Domain: app.rally.fun, Date: 2026-08-22, Symptom: Fails to handle social OAuth (X, GitHub) popup/redirect timeouts.
import asyncio
from playwright.async_api import Page, TimeoutError

async def handle_social_oauth(page: Page, trigger_selector: str, oauth_domain: str, auth_action_selector: str = None) -> bool:
    """
    Clicks a social login trigger and handles the resulting OAuth popup or redirect generically.
    """
    try:
        async with page.context.expect_page(timeout=10000) as page_info:
            await page.click(trigger_selector)
        popup = await page_info.value
        await popup.wait_for_load_state('domcontentloaded')
        if auth_action_selector:
            await popup.click(auth_action_selector)
        await popup.wait_for_event('close', timeout=30000)
        return True
    except TimeoutError:
        if oauth_domain in page.url:
            if auth_action_selector:
                await page.click(auth_action_selector)
            await page.wait_for_url(lambda url: oauth_domain not in url, timeout=30000)
            return True
    except Exception as e:
        print(f"OAuth handler error: {e}")
    return False
