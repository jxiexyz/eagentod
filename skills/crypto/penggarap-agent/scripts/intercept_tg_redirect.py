# Metadata: Domain: join.actionmodel.com, Date: 2026-08-27, Symptom: t.me links blocked in precheck causing navigation failures
import asyncio

async def execute(page, target_domain="t.me"):
    extracted_urls = []

    async def intercept_request(route):
        url = route.request.url
        if target_domain in url or url.startswith("tg://"):
            extracted_urls.append(url)
            await route.abort("blockedbyclient")
        else:
            await route.continue_()

    await page.route("**/*", intercept_request)

    # Check existing DOM links
    dom_links = await page.evaluate(f'''() => {{
        return Array.from(document.querySelectorAll("a"))
            .map(a => a.href)
            .filter(href => href.includes("{target_domain}") || href.startsWith("tg://"));
    }}''')
    extracted_urls.extend(dom_links)

    # Allow time for potential JS auto-redirects
    await asyncio.sleep(2.5)
    
    try:
        await page.unroute("**/*", intercept_request)
    except Exception:
        pass

    if extracted_urls:
        return {"status": "success", "links": list(set(extracted_urls))}
    return {"status": "failed", "reason": "No matching links found or intercepted"}