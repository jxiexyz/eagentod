# Metadata: withspout.com, 2026-08-17, hermes -z no final response
from playwright.async_api import Page

async def safe_interact(page: Page, selector: str, action: str = 'click', timeout: int = 5000) -> bool:
    try:
        loc = page.locator(selector).first
        await loc.wait_for(state="attached", timeout=timeout)
        await getattr(loc, action)(timeout=timeout, force=True)
        return True
    except Exception as e:
        print(f"Fail {selector}: {e}")
        return False