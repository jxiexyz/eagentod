# Metadata: Origin Domain: testnet.x1ecochain.com, Date: 2026-08-24, Symptom: Telegram bot requirement blocks web automation (t.me links blocked in precheck)

async def extract_tg_bot_links(page):
    """
    Extracts Telegram bot links from the page to be delegated to the Telegram worker.
    Prevents Playwright from hanging on blocked t.me/tg:// protocol links.
    """
    links = await page.evaluate('''() => {
        return Array.from(document.querySelectorAll('a'))
            .map(a => a.href)
            .filter(href => href.includes('t.me/') || href.includes('tg://'));
    }''')
    return list(set(links))
