# Metadata: Origin Domain: teogiwa.com, Date: 2026-08-24, Symptom: Social tasks require clicking sequentially before revealing dual X/EVM input submission form

import asyncio

async def solve_waitlist(page, x_username: str, evm_address: str, social_keywords=None, action_keywords=None):
    if social_keywords is None:
        social_keywords = ['Follow', 'Like', 'Repost', 'Retweet', 'Join', 'Verify']
    if action_keywords is None:
        action_keywords = ['Lay', 'Submit', 'Register', 'Enter', 'Confirm', 'Mint']

    # 1. Execute Social Tasks sequentially
    for kw in social_keywords:
        try:
            btns = await page.locator(f"button:has-text('{kw}'), a:has-text('{kw}')").all()
            for btn in btns:
                if await btn.is_visible():
                    await btn.click(force=True)
                    await page.wait_for_timeout(1500)
        except Exception as e:
            pass

    # 2. Click main action button to reveal form if necessary (e.g., 'Lay your tile')
    for kw in action_keywords:
        try:
            action_btns = await page.locator(f"button:has-text('{kw}'), a:has-text('{kw}')").all()
            for btn in action_btns:
                if await btn.is_visible():
                    await btn.click(force=True)
                    await page.wait_for_timeout(1500)
        except:
            pass

    # 3. Inject X Username
    try:
        inputs = await page.locator("input[type='text'], input:not([type])").all()
        for inp in inputs:
            ph = (await inp.get_attribute("placeholder") or "").lower()
            # Try to get surrounding text for context
            context = await inp.evaluate("el => { let text = ''; if (el.previousElementSibling) text += el.previousElementSibling.innerText; if (el.parentElement) text += el.parentElement.innerText; return text.toLowerCase(); }")
            if "username" in ph or "x " in ph or "@" in ph or "username" in context or "twitter" in context:
                await inp.fill("")
                await inp.type(x_username, delay=50)
                await inp.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
                break
    except Exception as e:
        pass

    # 4. Inject EVM Address
    try:
        inputs = await page.locator("input[type='text'], input:not([type])").all()
        for inp in inputs:
            ph = (await inp.get_attribute("placeholder") or "").lower()
            context = await inp.evaluate("el => { let text = ''; if (el.previousElementSibling) text += el.previousElementSibling.innerText; if (el.parentElement) text += el.parentElement.innerText; return text.toLowerCase(); }")
            if "0x" in ph or "address" in ph or "evm" in ph or "wallet" in ph or "0x" in context or "address" in context:
                await inp.fill("")
                await inp.type(evm_address, delay=50)
                await inp.evaluate("el => el.dispatchEvent(new Event('input', { bubbles: true }))")
                break
    except Exception as e:
        pass

    # 5. Submit Form
    for kw in action_keywords:
        try:
            sub_btns = await page.locator(f"button:has-text('{kw}')").all()
            for btn in sub_btns:
                if await btn.is_visible() and not await btn.is_disabled():
                    await btn.click(force=True)
                    await page.wait_for_timeout(2000)
                    return True
        except Exception:
            pass
            
    return True
