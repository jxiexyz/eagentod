# Metadata
# Origin Domain: mudlarknft.com
# Date: 2026-08-21
# Specific Symptom: Fails to interact with X/Twitter OAuth authorization popup window during account connection.

import asyncio

async def handle_x_oauth_popup(page, trigger_selector: str = None):
    """
    Handles the X/Twitter OAuth popup bypassing new page context tracking issues.
    Optionally clicks a trigger button if provided.
    """
    try:
        if trigger_selector:
            async with page.context.expect_page() as new_page_info:
                await page.click(trigger_selector)
            popup = await new_page_info.value
        else:
            pages = page.context.pages
            popup = next((p for p in pages if "twitter.com" in p.url or "x.com" in p.url and "oauth" in p.url), None)
            if not popup:
                raise Exception("X OAuth popup not found in current context.")

        await popup.wait_for_load_state("domcontentloaded")
        
        authorize_btn = popup.locator("[data-testid='OAuth_Consent_Button'], button:has-text('Authorize app')").first
        
        if await authorize_btn.is_visible(timeout=10000):
            await authorize_btn.click()
            try:
                await popup.wait_for_event("close", timeout=15000)
            except:
                pass
            return True
        else:
            print("Authorize button not found on X popup.")
            return False
            
    except Exception as e:
        print(f"Error handling X OAuth popup: {e}")
        return False
