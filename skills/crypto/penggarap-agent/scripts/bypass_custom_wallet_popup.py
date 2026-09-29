# Metadata: quest.unicity.network, 2026-08-21, Custom web wallet popup authorization handshake failure
import asyncio
from playwright.async_api import Page, TimeoutError

async def bypass_custom_wallet_popup(page: Page, connect_selector: str, authorize_selector: str, popup_url_pattern: str = ""):
    """
    Generic bypass for web-based custom wallets that open in a new tab/popup.
    Clicks connect, intercepts the popup, clicks authorize, and waits for handshake completion.
    """
    context = page.context
    popup_future = asyncio.Future()
    
    def on_page(new_page):
        if not popup_future.done():
            popup_future.set_result(new_page)
            
    context.on("page", on_page)
    
    popup = None
    for p in context.pages:
        if p != page and (popup_url_pattern in p.url if popup_url_pattern else True):
            popup = p
            break
            
    if not popup:
        await page.wait_for_selector(connect_selector, state="visible", timeout=15000)
        await page.click(connect_selector)
        try:
            popup = await asyncio.wait_for(popup_future, timeout=15000)
        except TimeoutError:
            context.remove_listener("page", on_page)
            for p in context.pages:
                if p != page and (popup_url_pattern in p.url if popup_url_pattern else True):
                    popup = p
                    break
            if not popup:
                raise Exception("Wallet popup did not appear after interaction.")
                
    context.remove_listener("page", on_page)
    
    await popup.wait_for_load_state("domcontentloaded")
    
    await popup.wait_for_selector(authorize_selector, state="visible", timeout=20000)
    await popup.click(authorize_selector)
    
    try:
        await popup.wait_for_event("close", timeout=15000)
    except Exception:
        pass
        
    await page.bring_to_front()
    return page
