# Metadata: Origin Domain: teogiwa.com, Date: 2026-08-23, Symptom: Waitlist EVM address submission failure / Missing elements
import asyncio

async def execute_waitlist_bypass(page, evm_address: str):
    wallet_inputs = await page.locator("input[placeholder*='0x'], input[name*='wallet'], input[name*='address'], input[type='text']").all()
    for el in wallet_inputs:
        if await el.is_visible():
            await el.fill(evm_address)
            break
            
    action_buttons = await page.locator("button, a").all()
    for btn in action_buttons:
        text = await btn.text_content()
        if text and any(kw in text.lower() for kw in ['follow', 'join', 'task', 'verify']):
            try:
                if await btn.is_visible():
                    await btn.click(timeout=2000)
                    await asyncio.sleep(1)
            except Exception:
                continue
                
    submit_buttons = await page.locator("button[type='submit'], button:has-text('Submit'), button:has-text('Register'), button:has-text('Join')").all()
    for btn in submit_buttons:
        if await btn.is_visible():
            await btn.click(timeout=3000)
            break
