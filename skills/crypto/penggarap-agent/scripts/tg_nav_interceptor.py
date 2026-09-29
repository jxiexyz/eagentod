# Metadata: Origin Domain: puffins.fun, Date: 2026-08-22, Symptom: VPS hang on t.me links due to Tencent Cloud IP block

async def bypass_tg_navigation(page, target_domains=None):
    if target_domains is None:
        target_domains = ["t.me", "telegram.me"]
    
    captured_urls = []
    async def handle_route(route):
        url = route.request.url
        if any(d in url for d in target_domains):
            captured_urls.append(url)
            await route.abort("blockedbyclient")
        else:
            await route.continue_()
            
    await page.route("**/*", handle_route)
    
    hrefs = await page.evaluate(
        "(domains) => Array.from(document.querySelectorAll('a')).map(a => a.href).filter(h => domains.some(d => h.includes(d)))",
        target_domains
    )
    
    return {
        "captured_urls": captured_urls,
        "dom_hrefs": list(set(hrefs))
    }