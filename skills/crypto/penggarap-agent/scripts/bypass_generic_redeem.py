# Metadata: Domain: commonsmade.com, Date: 2026-08-24, Symptom: Input hidden until reveal button clicked, and delayed claim buttons.
import asyncio
from playwright.async_api import Page

async def execute_bypass(page: Page, target_url: str = None, redeem_code: str = "LOVE", reveal_selector: str = 'button.gate-reveal', **kwargs):
    """Generic bypass to reveal hidden inputs, fill a redeem/promo code, and handle delayed claim buttons."""
    if target_url and target_url not in page.url:
        await page.goto(target_url, wait_until="domcontentloaded")
        await page.wait_for_timeout(2000)

    # 1. Handle hidden gate/password overlays
    try:
        reveal_btn = await page.query_selector(reveal_selector)
        if reveal_btn:
            await reveal_btn.click()
            await page.wait_for_timeout(1000)
    except Exception:
        pass

    input_selectors = [
        "input[placeholder*='code' i]",
        "input[placeholder*='vouch' i]",
        "input[name*='code' i]",
        "#gate-password",
        "input[type='password']",
        "input[type='text']"
    ]
    
    input_element = None
    for sel in input_selectors:
        try:
            el = await page.wait_for_selector(sel, state="visible", timeout=2000)
            if el:
                input_element = el
                break
        except Exception:
            continue
            
    if input_element:
        await input_element.fill(redeem_code)
        await page.wait_for_timeout(500)
        await input_element.press("Enter")
        await page.wait_for_timeout(3000)
    
    # 2. Handle delayed claim buttons (e.g. counting up score)
    claim_selectors = [
        'button:has-text("Take my place")',
        'button._accept_2q2hc_67',
        'button:has-text("Claim")'
    ]
    
    for _ in range(15):
        for sel in claim_selectors:
            try:
                claim_btn = await page.query_selector(sel)
                if claim_btn:
                    is_disabled = await claim_btn.evaluate('el => el.disabled')
                    if not is_disabled:
                        await claim_btn.click()
                        await page.wait_for_timeout(2000)
                        return True
            except Exception:
                pass
        await page.wait_for_timeout(1000)

    return True