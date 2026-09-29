# Metadata: Origin Domain: app.zen-o.xyz, Date: 2026-08-23, Symptom: Waitlist social tasks and EVM form submission handling
import asyncio

async def complete_waitlist_tasks(page, evm_address: str):
    """
    Bypass script for standard waitlist forms requiring social clicks and EVM submission.
    Accepts generic page object to avoid hardcoded domains.
    """
    # 1. Handle social tasks (intercept tabs to avoid clutter/hangs)
    social_selectors = ['a[href*="twitter.com"]', 'a[href*="x.com"]', 'a[href*="t.me"]', 'button:has-text("Follow")', 'button:has-text("Verify")']
    for sel in social_selectors:
        elements = await page.query_selector_all(sel)
        for el in elements:
            try:
                async with page.context.expect_page(timeout=3000) as new_page_info:
                    await el.click(force=True)
                new_page = await new_page_info.value
                await asyncio.sleep(1)
                await new_page.close()
            except Exception:
                try:
                    await el.click(force=True)
                except:
                    pass
            await asyncio.sleep(1)

    # 2. Input EVM address
    evm_selectors = ['input[placeholder*="0x"]', 'input[placeholder*="address" i]', 'input[type="text"]']
    for sel in evm_selectors:
        inputs = await page.query_selector_all(sel)
        for inp in inputs:
            is_visible = await inp.is_visible()
            if is_visible:
                await inp.fill(evm_address)
                await asyncio.sleep(0.5)
                break

    # 3. Submit
    submit_selectors = ['button:has-text("Submit")', 'button:has-text("Join")', 'button:has-text("Register")']
    for sel in submit_selectors:
        btn = await page.query_selector(sel)
        if btn and await btn.is_visible():
            await btn.click(force=True)
            await asyncio.sleep(2)
            break

    return True
