# Metadata: Origin Domain: rewards.canopynetwork.org | Date: 2026-08-26 | Symptom: Social tasks disabled/unclickable or wallet submit hanging

async def bypass_social_and_submit(page, wallet_address, task_selectors=None, submit_selector="input[placeholder*='address' i], input[name*='wallet' i], input[type='text']"):
    """
    Generic bypass for social reward claims:
    1. Removes 'disabled' attributes from task verification buttons.
    2. Fills the wallet address.
    3. Attempts to click submit.
    """
    if task_selectors:
        for sel in task_selectors:
            try:
                await page.evaluate(f"""(selector) => {{
                    document.querySelectorAll(selector).forEach(el => {{
                        el.removeAttribute('disabled');
                        el.classList.remove('disabled');
                        el.classList.remove('opacity-50');
                        el.style.pointerEvents = 'auto';
                    }});
                }}""", sel)
                await page.click(sel, timeout=3000)
            except Exception as e:
                print(f"Skipped task selector {sel}: {e}")
                
    try:
        # Attempt to find and fill the wallet input
        await page.wait_for_selector(submit_selector, timeout=5000, state='attached')
        await page.fill(submit_selector, wallet_address)
        
        # Force click standard submit/claim buttons
        submit_btn = "button[type='submit'], button:has-text('Submit'), button:has-text('Claim'), button:has-text('Join')"
        await page.evaluate(f"""(sel) => {{
            let btn = document.querySelector(sel);
            if(btn) {{
                btn.removeAttribute('disabled');
                btn.click();
            }}
        }}""", submit_btn)
        return True
    except Exception as e:
        print(f"Failed wallet submission: {e}")
        return False
