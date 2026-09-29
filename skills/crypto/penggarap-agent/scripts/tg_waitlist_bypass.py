# Metadata: Domain: Generic (mlue.fun), Date: 2026-08-27, Symptom: Blocked on TG deep link extraction or waitlist button visibility

async def execute(page, selector="a[href*='t.me/'], a[href^='tg://']"):
    """Extracts Telegram bot link or bypasses overlay to click waitlist buttons."""
    try:
        await page.wait_for_selector(selector, state="attached", timeout=10000)
        href = await page.evaluate("(sel) => { const el = document.querySelector(sel); return el ? el.href : null; }", selector)
        if href:
            return {"success": True, "link": href}
        
        await page.evaluate("(sel) => { const el = document.querySelector(sel); if(el) el.click(); }", selector)
        return {"success": True, "action": "clicked"}
    except Exception as e:
        return {"success": False, "error": str(e)}
