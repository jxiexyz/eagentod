# Metadata: Domain: inkersnft.xyz, Date: 2026-08-24, Symptom: Task completion and EVM address submission blocking/failing

async def bypass_evm_task_submit(page, evm_address: str):
    """
    Generic Web3 task form solver. Bypasses standard Verify/Submit flows.
    """
    import asyncio

    # 1. Iterate and click generic verification/task buttons
    action_buttons = await page.locator('button:has-text("Verify"), button:has-text("Check"), button:has-text("Follow"), button:has-text("Join")').all()
    for btn in action_buttons:
        if await btn.is_visible():
            await btn.click()
            await asyncio.sleep(1.5)

    # 2. Locate EVM input field (shadow DOM piercing or placeholder heuristics)
    input_field = page.locator('input[placeholder*="0x" i], input[placeholder*="address" i]').first
    if await input_field.is_visible():
        await input_field.fill(evm_address)

    # 3. Submit application
    submit_btn = page.locator('button:has-text("Apply"), button:has-text("Submit")').first
    if await submit_btn.is_visible():
        await submit_btn.click()
        await asyncio.sleep(2.0)

    return True