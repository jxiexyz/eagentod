# Metadata: Origin Domain: inkclub.club, Date: 2026-08-24, Symptom: Social action (X follow/repost) and EVM address submission failure

import asyncio

async def bypass_social_evm_form(page, evm_address: str, timeout: int = 5000):
    """Reusable bypass for generic Web3 social forms and EVM inputs."""
    try:
        # 1. Broadly target EVM inputs via common placeholders/names
        evm_input = page.locator('input[placeholder*="0x" i], input[placeholder*="address" i], input[placeholder*="EVM" i], input[name*="address" i]').first
        await evm_input.wait_for(state="visible", timeout=timeout)
        await evm_input.fill(evm_address)
        
        # 2. Handle typical Twitter/X interaction buttons if they are stuck in pending states
        action_buttons = page.locator('button:has-text("Follow"), button:has-text("Repost"), button:has-text("Comment"), button:has-text("Verify")')
        count = await action_buttons.count()
        for i in range(count):
            btn = action_buttons.nth(i)
            if await btn.is_visible():
                await btn.click(force=True)
                await asyncio.sleep(1.5)
                
        # 3. Submit form
        submit_btn = page.locator('button[type="submit"], button:has-text("Submit"), button:has-text("Join")').first
        if await submit_btn.is_visible():
            await submit_btn.click(force=True)
            
        return True
    except Exception as e:
        print(f"[bypass_social_evm_form] Error: {e}")
        return False
