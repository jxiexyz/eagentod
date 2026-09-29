# Metadata: Origin Domain: chatlee.io, Date: 2026-08-21, Symptom: Email login and social task follow automation

async def bypass_email_and_follow(page, email: str, email_sel: str, submit_sel: str, follow_sel: str = None):
    """Handles standard email form submission and optional sequential click tasks."""
    try:
        await page.wait_for_selector(email_sel, state="visible", timeout=15000)
        await page.fill(email_sel, email)
        await page.click(submit_sel)
        
        if follow_sel:
            await page.wait_for_timeout(2000)
            follow_btns = await page.locator(follow_sel).all()
            for btn in follow_btns:
                if await btn.is_visible():
                    await btn.click()
                    await page.wait_for_timeout(1500)
        return True
    except Exception as e:
        print(f"Action failed: {e}")
        return False
