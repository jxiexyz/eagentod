# Metadata: linktr.ee, 2026-08-24, Cookie banner overlay and dynamic class names blocking click/extraction
import asyncio

async def run(page, target_texts=None):
    """
    Generic bypass to dismiss cookie overlays and extract/click target links.
    target_texts: list of strings to search for in link text.
    """
    accept_texts = ['Accept', 'Agree', 'Got it', 'Allow all', 'Accept All']
    for text in accept_texts:
        try:
            btn = await page.query_selector(f"button:has-text('{text}')")
            if btn and await btn.is_visible():
                await btn.click()
                await asyncio.sleep(1)
        except Exception:
            pass
    
    links = []
    elements = await page.query_selector_all("a")
    for el in elements:
        try:
            href = await el.get_attribute("href")
            text_content = await el.text_content()
            if href:
                links.append({"text": text_content.strip() if text_content else "", "href": href})
        except Exception:
            continue
            
    if target_texts:
        filtered = []
        for link in links:
            if any(t.lower() in link['text'].lower() for t in target_texts):
                filtered.append(link)
        return filtered
        
    return links
