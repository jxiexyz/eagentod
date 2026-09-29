# Metadata: Domain: join.actionmodel.com, Date: 2026-08-27, Symptom: t.me links blocked in precheck

async def execute(page, **kwargs):
    links = await page.evaluate("Array.from(document.querySelectorAll('a[href*=\"t.me\"]')).map(a => a.href)")
    if links:
        return {"success": True, "telegram_links": links}
    return {"success": False, "error": "t.me link not found"}