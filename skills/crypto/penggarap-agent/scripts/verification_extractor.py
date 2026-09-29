# Metadata: Domain: tsukinft.xyz, Date: 2026-08-19, Symptom: Worker claimed success but provided NO valid VERIFICATION artifact.
from playwright.async_api import Page, TimeoutError

async def extract_verification(page: Page, selectors: list[str] = None, timeout: int = 5000) -> str | None:
    """
    Waits for and extracts a verification artifact (text or tx link) from the DOM.
    Defaults to common success indicators if no selectors provided.
    """
    selectors = selectors or [
        "text='Success'",
        "text='Confirmed'",
        "text='Claimed'",
        ".Toastify__toast--success",
        "a[href*='tx/']",
        "a[href*='explorer']"
    ]
    for sel in selectors:
        try:
            el = await page.wait_for_selector(sel, state="attached", timeout=timeout)
            if el:
                href = await el.get_attribute("href")
                return href if href else (await el.inner_text()).strip()
        except TimeoutError:
            continue
    return None