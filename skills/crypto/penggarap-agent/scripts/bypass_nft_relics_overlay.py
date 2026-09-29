# Metadata: nft-relics.xyz, 2026-08-26, #pre overlay blocking interaction
import asyncio

async def bypass_nft_relics_overlay(page):
    """
    Dismisses the #pre intro overlay on nft-relics.xyz to allow interaction
    with the WL form.
    """
    await page.evaluate('''() => {
        const enterBtn = document.querySelector('#enterBtn');
        if (enterBtn) enterBtn.click();
        const preOverlay = document.querySelector('#pre');
        if (preOverlay) preOverlay.remove();
    }''')
    await asyncio.sleep(1)

