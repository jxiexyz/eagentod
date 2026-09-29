# Origin Domain: onchainsketches.xyz
# Date: 2026-08-27
# Symptom: EVM address submission failure on whitelist form

async def bypass_whitelist_form(page, address: str, input_sel: str = "input[type='text'], input[placeholder*='0x']"):
    input_loc = page.locator(input_sel).first
    await input_loc.wait_for(state="visible", timeout=10000)
    await input_loc.fill(address)
    await page.keyboard.press("Enter")
    await page.wait_for_timeout(2000)
    return True
