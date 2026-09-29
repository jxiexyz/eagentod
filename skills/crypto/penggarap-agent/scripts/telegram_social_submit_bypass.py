# Metadata: Origin Domain: inksideout.site, Date: 2026-08-27, Symptom: Social link navigation hangs on deep links (tg://) and wallet input times out
import asyncio

async def bypass_social_and_submit(page, wallet_address, social_selectors=['a[href*="t.me" i]', 'a[href*="twitter.com" i]', 'a[href*="x.com" i]', 'a[href*="tg://" i]'], input_selector='input[placeholder*="address" i], input[placeholder*="BSC" i], input[placeholder*="BEP20" i], input[placeholder*="0x" i]'):
    """
    Bypasses protocol handler hangs for social tasks and fills wallet address.
    """
    try:
        # Click the initial apply button if it exists
        apply_btn = page.locator("a:has-text('APPLY FOR WL'), button:has-text('APPLY FOR WL')")
        if await apply_btn.count() > 0 and await apply_btn.first.is_visible():
            await apply_btn.first.click(timeout=3000)
            await asyncio.sleep(2)
    except Exception as e:
        print(f"Skipped initial apply button: {e}")

    for sel in social_selectors:
        try:
            # Prevent page hangs on tg:// or external protocol links by stripping targets and href
            await page.evaluate(f"document.querySelectorAll('{sel}').forEach(el => {{ el.target = '_blank'; el.removeAttribute('href'); }})")
            await page.click(sel, timeout=3000, no_wait_after=True)
            await asyncio.sleep(1.5)
        except Exception as e:
            print(f"Skipped social task {sel}: {e}")
    
    try:
        await page.wait_for_selector(input_selector, state="visible", timeout=8000)
        await page.fill(input_selector, wallet_address)
        
        submit_btn = await page.query_selector('button[type="submit"], button:has-text("Submit"), button:has-text("Claim"), button:has-text("Verify"), button:has-text("Apply")')
        if submit_btn:
            await submit_btn.click()
        return True
    except Exception as e:
        print(f"Wallet submission failed: {e}")
        return False
