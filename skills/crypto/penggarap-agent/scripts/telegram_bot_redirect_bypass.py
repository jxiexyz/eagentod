# Metadata: Origin Domain: event.neosoul.ai, Date: 2026-08-22, Symptom: Headless browser crashes or hangs on t.me/tg:// deep links during Telegram bot redirects.
import re
from playwright.async_api import Page

async def extract_telegram_bot_link(page: Page, selector: str = "a[href*='t.me'], a[href*='tg://']"):
    """
    Bypasses navigation to t.me/tg deep links which hang headless browsers.
    Extracts the bot name and start parameter from the DOM without navigating.
    """
    try:
        # Prevent default click behavior on tg links to avoid unhandled protocol exceptions
        await page.evaluate('''() => {
            document.querySelectorAll("a[href*='t.me'], a[href*='tg://']").forEach(a => {
                a.addEventListener('click', e => {
                    e.preventDefault();
                    e.stopPropagation();
                });
            });
        }''')
        
        # Wait for element and extract href directly
        element = await page.wait_for_selector(selector, timeout=5000)
        if element:
            href = await element.get_attribute("href")
            bot_match = re.search(r'(?:t\.me/|tg://resolve\?domain=)([^?/]+)', href)
            start_match = re.search(r'start(?:app)?=([^&]+)', href)
            
            return {
                "raw_url": href,
                "bot_name": bot_match.group(1) if bot_match else None,
                "start_param": start_match.group(1) if start_match else None
            }
    except Exception as e:
        return {"error": str(e)}
    return None
