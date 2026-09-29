# Metadata: chatlee.io, 2026-08-21, Element click intercepted by overlay or dynamic load timeout
import asyncio

async def force_click(page, selector: str, timeout: int = 15000):
    """
    Waits for an element and forces a click via JS evaluation to bypass overlays and interceptions.
    """
    try:
        await page.wait_for_selector(selector, state='attached', timeout=timeout)
        await page.evaluate(f'''(sel) => {{
            const el = document.querySelector(sel);
            if (el) {{
                el.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                el.click();
            }}
        }}''', selector)
        return True
    except Exception as e:
        print(f"[Bypass Error] Failed to force click {selector}: {e}")
        return False
