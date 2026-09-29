# Origin Domain: hub.axisrobotics.ai
# Date: 2026-08-22
# Symptom: Worker agent hangs on social task completion and EVM address submission on hub platforms.

import asyncio

async def bypass_social_and_submit(page, evm_address, input_selector='input[placeholder*="0x"], input[name*="wallet"], input[name*="address"]', submit_selector='button:has-text("Submit"), button:has-text("Join"), button:has-text("Register")'):
    """
    Generic bypass to handle social task buttons (opening popups) and submitting EVM addresses.
    """
    # 1. Fill EVM if visible immediately
    try:
        input_locator = page.locator(input_selector).first
        await input_locator.wait_for(state="visible", timeout=5000)
        await input_locator.fill(evm_address)
    except Exception:
        pass

    # 2. Handle social tasks (popups)
    social_keywords = ['Twitter', ' X ', 'Discord', 'Connect', 'Follow', 'Retweet', 'Like']
    for keyword in social_keywords:
        try:
            btn = page.locator(f'button:has-text("{keyword}"), a:has-text("{keyword}")').first
            if await btn.is_visible():
                async with page.expect_popup(timeout=5000) as popup_info:
                    await btn.click()
                popup = await popup_info.value
                await popup.wait_for_load_state()
                await popup.close() # Close to simulate quick verification
                await asyncio.sleep(1)
        except Exception:
            continue

    # 3. Retry filling EVM if it appeared after social tasks
    try:
        input_locator = page.locator(input_selector).first
        if await input_locator.is_visible() and await input_locator.input_value() == '':
            await input_locator.fill(evm_address)
    except Exception:
        pass
        
    # 4. Submit form
    try:
        submit_btn = page.locator(submit_selector).first
        await submit_btn.wait_for(state="visible", timeout=5000)
        await submit_btn.click()
        await page.wait_for_load_state("networkidle", timeout=10000)
        return True
    except Exception as e:
        print(f"Submission failed: {e}")
        return False
