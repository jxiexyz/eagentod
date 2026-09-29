# Origin Domain: app.stabilizer.finance
# Date: 2026-08-24
# Symptom: Failure to register or inject referral code during onboarding.

import asyncio

async def inject_input_and_submit(page, input_selector: str, value: str, submit_selector: str = None):
    """
    Robustly injects text into an input field, circumventing standard Playwright .fill() blockers
    such as React synthetic events dropping characters or shadow DOM obscuring elements.
    """
    try:
        input_element = await page.wait_for_selector(input_selector, state="visible", timeout=10000)
        if not input_element:
            raise Exception(f"Selector {input_selector} not found.")

        await input_element.fill(value)
        await page.wait_for_timeout(500)
        
        current_value = await input_element.evaluate("el => el.value")
        if current_value != value:
            await page.evaluate('''([selector, val]) => {
                const el = document.querySelector(selector);
                if (el) {
                    let lastValue = el.value;
                    el.value = val;
                    let tracker = el._valueTracker;
                    if (tracker) { tracker.setValue(lastValue); }
                    el.dispatchEvent(new Event("input", { bubbles: true }));
                    el.dispatchEvent(new Event("change", { bubbles: true }));
                }
            }''', [input_selector, value])
            await page.wait_for_timeout(500)

        if submit_selector:
            submit_element = await page.wait_for_selector(submit_selector, state="visible", timeout=5000)
            if submit_element:
                try:
                    await submit_element.click(timeout=3000)
                except:
                    await submit_element.evaluate("el => el.click()")
                    
        return True
    except Exception as e:
        print(f"Bypass failed: {str(e)}")
        return False
