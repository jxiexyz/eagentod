# Metadata: Origin Domain: linktr.ee, Date: 2026-08-22, Symptom: Link extraction failure / cookie blocker
import asyncio

async def extract_linktree_links(page, target_text=None):
    """
    Bypasses cookie consent and extracts links from linktr.ee.
    If target_text is provided, clicks the link matching the text.
    Returns a list of dicts: [{'title': str, 'url': str}] or the specific clicked URL.
    """
    # Dismiss cookie consent if it appears
    try:
        cookie_btn = page.locator('button:has-text("Accept"), button:has-text("Agree"), button[aria-label="Accept"]')
        if await cookie_btn.count() > 0:
            await cookie_btn.first.click(timeout=3000)
    except Exception:
        pass
    
    # Wait for links to load
    try:
        await page.wait_for_selector('a[data-testid="LinkButton"]', timeout=10000)
    except Exception:
        return []
    
    links = []
    elements = await page.locator('a[data-testid="LinkButton"]').all()
    
    for el in elements:
        url = await el.get_attribute('href')
        title = await el.inner_text()
        links.append({'title': title.strip(), 'url': url})
        
        if target_text and target_text.lower() in title.lower():
            await el.click()
            return url
            
    return links
