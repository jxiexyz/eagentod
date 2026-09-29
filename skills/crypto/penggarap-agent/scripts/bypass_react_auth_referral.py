# Metadata: Origin Domain: teogiwa.com | Date: 2026-08-24 | Symptom: React/SPA register auth and referral code input dropping synthetic events
import asyncio

async def bypass_auth_and_referral(page, email: str, referral_code: str, email_selector: str, referral_selector: str, submit_selector: str):
    """
    Bypasses standard Playwright fill/click issues on React-based registration pages.
    Injects values directly and dispatches input events to trigger React state managers.
    """
    # 1. Force fill email
    if email and email_selector:
        await page.wait_for_selector(email_selector, state='visible', timeout=10000)
        await page.evaluate(f'''(selector, val) => {{
            const el = document.querySelector(selector);
            if(el) {{
                el.value = val;
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
        }}''', email_selector, email)
        await asyncio.sleep(0.5)
    
    # 2. Force fill referral code
    if referral_code and referral_selector:
        try:
            await page.wait_for_selector(referral_selector, state='visible', timeout=5000)
            await page.evaluate(f'''(selector, val) => {{
                const el = document.querySelector(selector);
                if(el) {{
                    el.value = val;
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}''', referral_selector, referral_code)
            await asyncio.sleep(0.5)
        except Exception as e:
            print(f"Bypass referral skipped: {e}")
            
    # 3. Force click submit avoiding pointer-events/z-index overlaps
    if submit_selector:
        await page.wait_for_selector(submit_selector, state='attached', timeout=5000)
        await page.evaluate(f'''(selector) => {{
            const el = document.querySelector(selector);
            if(el) el.click();
        }}''', submit_selector)
        
    await asyncio.sleep(3)
