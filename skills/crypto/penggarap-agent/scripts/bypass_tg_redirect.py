# Metadata: Domain: Generic (whitelist.brokedealershq.xyz), Date: 2026-08-27, Symptom: Navigation hangs on tg:// or t.me/ deep link redirects.
import re

async def extract_tg_bot_params(page, selector="a[href*='t.me/'], a[href*='tg://']"):
    """Extract TG bot parameters instead of clicking to avoid protocol handler hangs."""
    links = await page.evaluate(f'''(sel) => {{
        return Array.from(document.querySelectorAll(sel)).map(a => a.href);
    }}''', selector)
    
    for link in links:
        bot = re.search(r'(?:t\.me/|domain=)([^?&/]+)', link)
        start = re.search(r'start=([^&]+)', link)
        if bot:
            return {
                "bot": bot.group(1), 
                "start": start.group(1) if start else "", 
                "url": link
            }
    return None
