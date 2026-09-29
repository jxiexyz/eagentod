# Metadata: Origin Domain: digitsbt.ngrndrewards.com, Date: 2026-08-24, Symptom: Task completion and EVM input submission failure
import asyncio

async def execute_bypass(page, evm_address, task_selector="button:has-text('Task'), a:has-text('Follow'), a:has-text('Retweet'), a:has-text('Join')", input_selector="input[placeholder*='0x'], input[name*='address'], input[type='text']", submit_selector="button:has-text('Submit'), button:has-text('Apply'), button:has-text('Claim')"):
    try:
        # 1. Force click all task buttons to trigger popups/completion states
        task_buttons = await page.locator(task_selector).all()
        for btn in task_buttons:
            if await btn.is_visible():
                await btn.evaluate("node => node.click()")
                await asyncio.sleep(1.0)

        # 2. Inject EVM address directly via JS to bypass React synthetic event blocks
        input_locator = page.locator(input_selector).first
        await input_locator.wait_for(state='attached', timeout=5000)
        await input_locator.evaluate(f"""(el) => {{
            el.value = '{evm_address}';
            let tracker = el._valueTracker;
            if (tracker) {{ tracker.setValue(''); }}
            el.dispatchEvent(new Event('input', {{ bubbles: true }}));
            el.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }}""")

        # 3. Force click submit button
        submit_btn = page.locator(submit_selector).first
        await submit_btn.wait_for(state='attached', timeout=5000)
        await submit_btn.evaluate("node => node.click()")
        
        return True
    except Exception as e:
        print(f"Bypass failed: {e}")
        return False
