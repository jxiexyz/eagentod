# Metadata: Domain: linktr.ee, Date: 2026-08-24, Symptom: Cookie banners/overlays intercepting clicks
import asyncio

async def bypass_overlays_and_click(page, target_text=None, target_href=None):
    overlays = [
        '#onetrust-consent-sdk',
        '[data-testid="CookieNotice"]',
        '.cookie-banner',
        'div[role="dialog"]',
        'div[aria-modal="true"]'
    ]
    for selector in overlays:
        try:
            await page.evaluate('(sel) => { document.querySelectorAll(sel).forEach(el => el.remove()); }', selector)
        except Exception:
            pass
    
    if target_text:
        await page.click(f'text={target_text}', force=True)
    elif target_href:
        await page.click(f'a[href*="{target_href}"]', force=True)
    
    return True
