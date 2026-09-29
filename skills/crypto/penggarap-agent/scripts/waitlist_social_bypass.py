# Metadata: Origin Domain: app.zen-o.xyz, Date: 2026-08-23, Symptom: Social task completion and EVM waitlist submission failures
import asyncio

async def solve_waitlist(page, evm_address, social_keywords=None, submit_keywords=None):
    if social_keywords is None:
        social_keywords = ['Connect', 'Follow', 'Verify', 'Join', 'Retweet', 'Like']
    if submit_keywords is None:
        submit_keywords = ['Submit', 'Join', 'Register', 'Enter']

    # 1. Execute Social Tasks
    for kw in social_keywords:
        try:
            btns = await page.locator(f"button:has-text('{kw}'), a:has-text('{kw}')").all()
            for btn in btns:
                if await btn.is_visible():
                    await btn.click(force=True)
                    await page.wait_for_timeout(2000)
        except Exception as e:
            print(f"Skip {kw}: {e}")

    # 2. Inject EVM Address
    try:
        inputs = await page.locator("input").all()
        for inp in inputs:
            ph = await inp.get_attribute("placeholder") or ""
            if "0x" in ph.lower() or "address" in ph.lower() or "wallet" in ph.lower() or "evm" in ph.lower():
                await inp.fill(evm_address)
                break
        else:
            # Fallback to first text input if no placeholder match
            text_inputs = await page.locator("input[type='text']").all()
            if text_inputs:
                await text_inputs[0].fill(evm_address)
    except Exception as e:
        print(f"EVM input error: {e}")

    # 3. Submit Form
    for kw in submit_keywords:
        try:
            sub_btn = page.locator(f"button:has-text('{kw}')").first
            if await sub_btn.is_visible(timeout=2000):
                await sub_btn.click()
                await page.wait_for_timeout(2000)
                break
        except Exception:
            pass
