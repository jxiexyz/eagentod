# Metadata: Origin Domain: Generic, Date: 2026-08-21, Symptom: Telegram redirect blocking automation

async def extract_tg_link(page, selector="a"):
    try:
        return await page.evaluate("(s) => Array.from(document.querySelectorAll(s)).map(a => a.href).filter(h => h.includes('t.me') || h.includes('tg://'))", selector)
    except Exception:
        return []
