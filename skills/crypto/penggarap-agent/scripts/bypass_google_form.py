# Metadata: docs.google.com, 2026-08-25, Form Submit button click timeout/failure on dynamic forms
import asyncio

async def bypass_form_submit(page, button_texts=("submit", "next", "kirim", "berikutnya")):
    for text in button_texts:
        btn = await page.query_selector(f'xpath=//div[@role="button"][contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{text}")]')
        if btn and await btn.is_visible():
            await btn.scroll_into_view_if_needed()
            await btn.click()
            try:
                await page.wait_for_load_state("networkidle", timeout=3000)
            except Exception:
                pass
            return True
    return False
