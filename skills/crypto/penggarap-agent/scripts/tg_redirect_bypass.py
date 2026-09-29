# Metadata: Domain: Generic (mlue.fun context), Date: 2026-08-27, Symptom: Cannot transition from web waitlist to Telegram bot due to unhandled app redirect prompts hanging Playwright.

async def extract_telegram_start_link(page, fallback_selector='a:has-text("Telegram"), a[href*="t.me"], a[href^="tg://"]'):
    """
    Intercepts and extracts the Telegram deep link (t.me/... or tg://...) without hanging Playwright on external app prompts.
    """
    tg_url = None

    def request_handler(request):
        nonlocal tg_url
        if request.url.startswith('tg://') or 't.me/' in request.url:
            tg_url = request.url

    page.on('request', request_handler)

    try:
        # Check DOM directly first
        hrefs = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('a'))
                .map(a => a.href)
                .filter(href => href.includes('t.me/') || href.startsWith('tg://'));
        }''')

        if hrefs:
            return hrefs[0]

        # Fallback: click target and intercept network request
        btn = page.locator(fallback_selector).first
        if await btn.count() > 0 and await btn.is_visible():
            await btn.click(no_wait_after=True)
            await page.wait_for_timeout(2000)

    except Exception as e:
        print(f"Bypass error: {e}")
    finally:
        page.remove_listener('request', request_handler)

    return tg_url
