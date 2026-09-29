# Metadata: Origin Domain: otterink.xyz, Date: 2026-08-25, Symptom: Quest completion button unclickable (Session 20260825_232448_d54700)

from playwright.async_api import Page

async def bypass_quest_click(page: Page, selector: str) -> bool:
    """Force click to bypass transparent overlays and strict actionability checks."""
    try:
        element = await page.wait_for_selector(selector, state="attached", timeout=5000)
        if element:
            # Bypass Playwright actionability checks completely via native DOM click
            await page.evaluate("(el) => el.click()", element)
            return True
    except Exception as e:
        print(f"Direct DOM click failed: {e}")
        try:
            # Fallback to Playwright force click
            await page.locator(selector).first.click(force=True)
            return True
        except Exception as e2:
            print(f"Force click fallback failed: {e2}")
    return False
