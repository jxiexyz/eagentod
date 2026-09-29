# Metadata: Origin Domain: kaito.ai, Date: 2026-08-21, Specific Symptom: Fails to handle X share popup and extract the exclusive short link for campaign participation.
import urllib.parse

async def extract_x_share_intent(page, share_button_selector: str, timeout: int = 10000):
    """
    Clicks a share button, intercepts the X/Twitter intent URL popup,
    extracts the pre-filled text and shortlink, and closes the popup.
    """
    async with page.expect_popup(timeout=timeout) as popup_info:
        await page.click(share_button_selector)
    
    popup = await popup_info.value
    await popup.wait_for_load_state('domcontentloaded')
    intent_url = popup.url
    await popup.close()
    
    parsed = urllib.parse.urlparse(intent_url)
    params = urllib.parse.parse_qs(parsed.query)
    
    text = params.get('text', [''])[0]
    url = params.get('url', [''])[0]
    
    return f"{text} {url}".strip()
