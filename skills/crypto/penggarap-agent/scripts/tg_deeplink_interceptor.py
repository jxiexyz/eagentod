# Metadata: Origin Domain: mlue.fun, Date: 2026-08-27, Symptom: Playwright crash on tg:// redirect or failure to extract t.me waitlist bot link.
import asyncio

async def extract_tg_bot_link(page, cta_selector: str, timeout: int = 15000) -> str:
    """
    Intercepts tg:// or t.me/ redirects to prevent ERR_UNKNOWN_URL_SCHEME.
    Extracts the destination URL for the Telegram Worker.
    """
    tg_link = None
    
    async def handle_route(route):
        nonlocal tg_link
        url = route.request.url
        if "t.me/" in url or url.startswith("tg://"):
            tg_link = url
            await route.abort()
        else:
            await route.continue_()
            
    await page.route("**/*", handle_route)
    
    try:
        await page.click(cta_selector)
        await page.wait_for_timeout(3000)
    except Exception:
        pass
    finally:
        try:
            await page.unroute("**/*", handle_route)
        except Exception:
            pass
        
    if not tg_link:
        try:
            href = await page.get_attribute(cta_selector, "href", timeout=1000)
            if href and ("t.me/" in href or href.startswith("tg://")):
                tg_link = href
        except Exception:
            pass
            
    return tg_link