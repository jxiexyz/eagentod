# Metadata: inkpunk.xyz, 2026-08-24, Social tasks and EVM address submission failure
import asyncio
import re

async def run_bypass(page, evm_address: str):
    """Bypass for generic social task clicking and EVM form filling."""
    # 1. Click social/verify buttons (ignores popup blocks)
    social_regex = re.compile(r'(follow|join|verify|connect|retweet|post)', re.I)
    for button in await page.get_by_role("button").all():
        if await button.is_visible():
            text = await button.text_content() or ""
            if social_regex.search(text):
                try:
                    await button.click(timeout=2000)
                    await asyncio.sleep(1)
                except Exception:
                    pass

    # 2. Fill EVM Address
    evm_regex = re.compile(r'(address|evm|wallet|0x)', re.I)
    inputs = await page.locator("input").all()
    filled = False
    for inp in inputs:
        if await inp.is_visible():
            ph = await inp.get_attribute("placeholder") or ""
            name = await inp.get_attribute("name") or ""
            if evm_regex.search(ph) or evm_regex.search(name):
                await inp.fill(evm_address)
                filled = True
                break
    
    if not filled:
        # Fallback to first visible textbox
        for inp in inputs:
            if await inp.is_visible():
                await inp.fill(evm_address)
                break

    # 3. Submit
    submit_regex = re.compile(r'(submit|join|register|enter|whitelist)', re.I)
    for button in await page.get_by_role("button").all():
        if await button.is_visible():
            text = await button.text_content() or ""
            if submit_regex.search(text):
                try:
                    await button.click(timeout=3000)
                    await asyncio.sleep(2)
                    break
                except Exception:
                    pass
