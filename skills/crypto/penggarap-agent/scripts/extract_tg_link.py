# Metadata: Origin Domain: testnet.x1ecochain.com, Date: 2026-08-24, Symptom: Fails to start Telegram bot from web UI due to deep link navigation blocks.

async def extract_telegram_bot_link(page):
    """
    Extracts Telegram bot link (t.me) from the page to bypass browser deep-linking blocks.
    Worker should pass this link directly to the Telegram API instead of clicking it.
    """
    try:
        links = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a'))
                .map(a => a.href)
                .filter(href => href.includes('t.me/'));
        }''')
        
        for link in links:
            if 'start=' in link.lower() or 'bot' in link.lower():
                return link
                
        return links[0] if links else None
    except Exception as e:
        print(f"Error extracting TG link: {e}")
        return None