# Metadata: Origin Domain: inklords.xyz, Date: 2026-08-24, Symptom: Fails to handle Telegram bot start/redirects
import re
from playwright.async_api import Page

async def extract_and_start_tg_bot(page: Page, tg_client=None, selector: str = 'a[href*="t.me"], a[href*="tg://"]'):
    """
    Finds Telegram bot links, extracts username/start param, and optionally starts it.
    """
    links = await page.locator(selector).all()
    for link in links:
        href = await link.get_attribute('href')
        if not href:
            continue
        
        bot_username, start_param = None, None
        if 't.me/' in href:
            parts = href.split('t.me/')[-1].split('?')
            bot_username = parts[0].replace('/', '')
            if len(parts) > 1 and 'start=' in parts[1]:
                start_param = parts[1].split('start=')[-1].split('&')[0]
        elif 'tg://resolve' in href:
            domain_match = re.search(r'domain=([^&]+)', href)
            start_match = re.search(r'start=([^&]+)', href)
            if domain_match:
                bot_username = domain_match.group(1)
            if start_match:
                start_param = start_match.group(1)
                
        if bot_username:
            if tg_client:
                await tg_client.send_message(bot_username, f'/start {start_param}' if start_param else '/start')
                return {"status": "started", "bot": bot_username, "start_param": start_param}
            return {"status": "extracted", "bot": bot_username, "start_param": start_param, "href": href}
            
    return {"status": "not_found"}
