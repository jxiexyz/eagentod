# Metadata: Domain: Generic (Triggered by event.neosoul.ai), Date: 2026-08-22, Symptom: t.me links hang VPS due to Tencent Cloud blocking Telegram API.

from playwright.async_api import Page
import re

async def execute(page: Page, **kwargs) -> dict:
    """
    Intercepts browser navigation to Telegram links to prevent VPS hangs.
    Captures the bot URL and payload so orchestrator can delegate to Telegram CLI.
    """
    captured_urls = []

    async def intercept_tg(route):
        url = route.request.url
        if "t.me/" in url or "telegram.me/" in url or url.startswith("tg://"):
            captured_urls.append(url)
            print(f"[Bypass] Intercepted blocked Telegram navigation: {url}")
            await route.abort()
        else:
            await route.continue_()

    # Route all traffic to catch redirects or programmatic navigations to Telegram
    await page.route("**/*", intercept_tg)
    
    return {
        "status": "success",
        "bypassed": True,
        "captured_telegram_urls": captured_urls,
        "action_required": "delegate_to_telegram_worker"
    }
