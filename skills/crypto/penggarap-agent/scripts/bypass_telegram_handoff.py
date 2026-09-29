# Metadata: Domain Generic, Date 2026-08-24, Symptom Handoff to TG Bot blocked/hanging
import re

async def execute(page, selector="a[href*='t.me/']", timeout=5000):
    try:
        try:
            await page.wait_for_selector(selector, timeout=timeout)
        except Exception:
            pass
        
        links = await page.evaluate('(sel) => Array.from(document.querySelectorAll(sel)).map(a => a.href)', selector)
        
        if links:
            return {"status": "success", "tg_link": links[0]}
            
        content = await page.content()
        matches = re.findall(r'(https?://t\.me/[^\s\'"<]+)', content)
        if matches:
            return {"status": "success", "tg_link": matches[0]}
            
        return {"status": "failed", "reason": "No Telegram links found"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
