# Origin Domain: rewards.canopynetwork.org
# Date: 2026-08-26
# Symptom: VPS browser hangs when navigating to t.me or tg:// URLs during bot/social tasks.

import re
from urllib.parse import urlparse, parse_qs

async def intercept_telegram_links(page):
    """
    Intercepts t.me and tg:// navigations to prevent VPS hanging.
    Returns a list of extracted bot targets and start parameters for backend CLI execution.
    """
    extracted_tg_tasks = []

    async def block_tg_route(route):
        url = route.request.url
        parsed = urlparse(url)
        bot, start_param = "", ""
        
        if url.startswith("tg://"):
            qs = parse_qs(parsed.query)
            bot = qs.get("domain", [""])[0]
            start_param = qs.get("start", [""])[0]
        else:
            path_parts = parsed.path.strip("/").split("/")
            bot = path_parts[0] if path_parts else ""
            qs = parse_qs(parsed.query)
            start_param = qs.get("start", [""])[0]
            
        if bot:
            extracted_tg_tasks.append({"bot": bot, "start": start_param})
        await route.abort()

    # Intercept both HTTP t.me links and native tg:// protocol links
    await page.route(re.compile(r"(https?://t\.me/|tg://)"), block_tg_route)
    return extracted_tg_tasks

async def submit_generic_address(page, input_selector: str, submit_selector: str, address: str):
    """
    Generic wallet address filler to avoid hardcoded domain logic.
    """
    await page.wait_for_selector(input_selector, state="visible", timeout=10000)
    await page.fill(input_selector, address)
    await page.click(submit_selector)
