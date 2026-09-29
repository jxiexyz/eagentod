# Metadata: Origin Domain: inkersnft.xyz, Date: 2026-08-24, Symptom: React/Web3 form failing to register EVM address input or locate submit button
import asyncio

async def bypass_evm_submit(page, address: str, input_selector: str = "input[placeholder*='0x'], input[name*='address']", submit_selector: str = "button:has-text('Submit'), button:has-text('Apply')"):
    try:
        await page.wait_for_selector(input_selector, state='visible', timeout=10000)
        await page.fill(input_selector, address)
        await page.evaluate('(sel) => { const el = document.querySelector(sel); if(el) { el.dispatchEvent(new Event("input", { bubbles: true })); el.dispatchEvent(new Event("change", { bubbles: true })); } }', input_selector)
        await asyncio.sleep(0.5)
        await page.click(submit_selector)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
