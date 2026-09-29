# Metadata: qms.finance, 2026-08-27, Cloudflare Turnstile blocking form submission
import asyncio
from playwright.async_api import Page

async def execute(page: Page, **kwargs):
    """
    Attempts to solve Cloudflare Turnstile widget by locating its iframe
    and clicking on it, then waiting for the hidden response token.
    """
    try:
        print("Attempting to bypass Turnstile...")
        iframe_element = await page.wait_for_selector('iframe[src*="turnstile"]', state='visible', timeout=10000)
        if iframe_element:
            box = await iframe_element.bounding_box()
            if box:
                # Click inside the iframe bounding box to trigger interactive challenges
                await page.mouse.click(box['x'] + 30, box['y'] + box['height'] / 2)
                
                # Wait for the token input to be populated
                await page.wait_for_function('''() => {
                    const input = document.querySelector('[name="cf-turnstile-response"]');
                    return input && input.value && input.value.length > 0;
                }''', timeout=15000)
                
                print("Turnstile solved successfully.")
                return True
    except Exception as e:
        print(f"Turnstile bypass failed or widget not present: {e}")
    return False
