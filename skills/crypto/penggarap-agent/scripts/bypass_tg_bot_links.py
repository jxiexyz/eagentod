# Origin Domain: testnet.x1ecochain.com
# Date: 2026-08-24
# Specific Symptom: VPS browser hangs on t.me links; need to extract bot and start token cleanly without navigation.

import urllib.parse
import logging

async def extract_and_block_tg_links(page):
    extracted_data = []

    async def route_handler(route):
        url = route.request.url
        if "t.me/" in url or "telegram.me/" in url:
            logging.info(f"Blocked TG navigation: {url}")
            await route.abort()
        else:
            await route.continue_()

    await page.route("**/*", route_handler)

    links = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(href => href.includes('t.me/') || href.includes('telegram.me/'));
    }''')

    for link in links:
        parsed = urllib.parse.urlparse(link)
        bot_name = parsed.path.strip('/')
        
        query = parsed.query
        start_token = ""
        if "start=" in query:
            start_token = urllib.parse.parse_qs(query).get("start", [""])[0]
        elif query.startswith("start"):
            start_token = query[5:]
            
        if bot_name:
            extracted_data.append({
                "bot": bot_name,
                "start": start_token,
                "raw_url": link
            })

    return extracted_data
