# Metadata: Origin Domain: allscale.io (Generic), Date: 2026-08-24, Symptom: Fails to process Telegram bot interactions (tg:// or t.me/ links)
import urllib.parse

async def extract_tg_intent(page, selector='a[href*="tg://"], a[href*="t.me/"]'):
    """Extracts bot username and payload for delegation to Telegram CLI."""
    try:
        await page.wait_for_selector(selector, timeout=5000)
        href = await page.evaluate('(sel) => document.querySelector(sel)?.href', selector)
        
        if not href:
            return {"error": "Link element found but no href"}
            
        bot_name, start_param = None, None
        parsed = urllib.parse.urlparse(href)
        qs = urllib.parse.parse_qs(parsed.query)
        
        if 'tg://' in href:
            bot_name = qs.get('domain', [None])[0]
            start_param = qs.get('start', [None])[0]
        else:
            parts = parsed.path.strip('/').split('/')
            bot_name = parts[0] if parts else None
            start_param = qs.get('start', [None])[0]
            
        return {"bot_name": bot_name, "start_param": start_param, "raw_url": href}
    except Exception as e:
        return {"error": str(e)}
