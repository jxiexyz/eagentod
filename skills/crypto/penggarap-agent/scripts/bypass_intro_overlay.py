# Origin Domain: nft-relics.xyz
# Date: 2026-08-26
# Specific Symptom: Intro overlay and its dismiss button block interactions with the main page.

import asyncio

async def bypass_intro_overlay(page, enter_btn_selector: str = '#enterBtn', overlay_selector: str = '#pre'):
    """
    Dismisses an intro overlay to allow interaction with the main page elements.
    """
    await page.evaluate(f'''() => {{
        const enterBtn = document.querySelector("{enter_btn_selector}");
        if (enterBtn) enterBtn.click();
        const preOverlay = document.querySelector("{overlay_selector}");
        if (preOverlay) preOverlay.remove();
    }}''')
    await asyncio.sleep(1)
