# Metadata: Domain: linktr.ee (Generic Profile Aggregator), Date: 2026-08-22, Symptom: Link extraction failure on aggregator profiles

async def extract_links(page, target_keywords=None):
    """
    Extracts links from a profile aggregator page.
    :param page: Playwright page object
    :param target_keywords: List of strings to filter URLs (e.g., ['t.me', 'x.com', 'gleam.io'])
    """
    await page.wait_for_load_state('networkidle', timeout=10000)
    
    try:
        await page.wait_for_selector('a[href]', timeout=5000)
    except Exception:
        pass # Proceed with evaluation even if timeout occurs, might be shadow DOM or delayed render

    links = await page.evaluate('''() => {
        const anchors = Array.from(document.querySelectorAll('a[href]'));
        return anchors.map(a => ({
            text: a.innerText.trim(),
            url: a.href
        }));
    }''')

    if target_keywords:
        return [link for link in links if any(k.lower() in link['url'].lower() for k in target_keywords)]
    
    return links
