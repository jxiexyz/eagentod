# Origin Domain: puffins.fun
# Date: 2026-08-21
# Specific Symptom: Task completion and EVM address input intercepted or blocked by generic overlays

async def run_bypass(page, evm_address=""):
    # 1. Nuke invisible/transparent overlays blocking clicks
    await page.evaluate('''() => {
        document.querySelectorAll('*').forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed' && style.zIndex > 999 && el.innerText.trim() === '') {
                el.remove();
            }
        });
    }''')
    
    # 2. Force click all standard task interaction buttons
    task_selectors = ['button:has-text("Follow")', 'button:has-text("Verify")', 'button:has-text("Check")', 'button:has-text("Start")', 'a:has-text("Join")']
    for sel in task_selectors:
        for el in await page.locator(sel).all():
            try:
                await el.evaluate("node => node.removeAttribute('disabled')")
                await el.click(force=True)
                await page.wait_for_timeout(1500)
            except:
                continue

    # 3. Locate EVM input field via permissive fuzzy matching and fill
    input_loc = page.locator('input[placeholder*="0x" i], input[placeholder*="Address" i], input[name*="wallet" i]').first
    if await input_loc.count() > 0:
        await input_loc.fill(evm_address)
        
    # 4. Trigger Submission
    submit = page.locator('button:has-text("Submit")', 'button:has-text("Claim")', 'button:has-text("Done")').first
    if await submit.count() > 0:
        await submit.evaluate("node => node.removeAttribute('disabled')")
        await submit.click(force=True)
        
    return True
