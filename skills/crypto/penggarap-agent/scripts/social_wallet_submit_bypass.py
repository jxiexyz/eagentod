# Origin Domain: di.xyz
# Date: 2026-08-27
# Specific Symptom: Automation gets stuck on social task verification popups and BSC address input during check-in.

import asyncio

async def bypass_social_and_submit(page, task_btn_selector, wallet_input_selector, submit_selector, wallet_address):
    """
    Generic bypass for social task lists and wallet submission.
    Clicks task buttons, handles new tabs, returns to main page, fills wallet.
    """
    tasks = await page.query_selector_all(task_btn_selector)
    for task in tasks:
        try:
            await task.scroll_into_view_if_needed()
            await task.click()
            await asyncio.sleep(2)
        except Exception as e:
            print(f"Task click failed: {e}")

    # Close spawned tabs
    if hasattr(page, 'context') and len(page.context.pages) > 1:
        for p in page.context.pages:
            if p != page:
                await p.close()
    await page.bring_to_front()

    # Fill wallet
    if wallet_input_selector and wallet_address:
        wallet_in = await page.wait_for_selector(wallet_input_selector, state='visible', timeout=5000)
        if wallet_in:
            await wallet_in.fill(wallet_address)

    # Submit
    if submit_selector:
        submit_btn = await page.wait_for_selector(submit_selector, state='visible', timeout=5000)
        if submit_btn:
            await submit_btn.click()
            await asyncio.sleep(2)

    return True
