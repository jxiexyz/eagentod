# Metadata: Domain: octra.fun, Date: 2026-08-26, Symptom: t.me navigations hang the VPS browser precheck
from urllib.parse import urlparse, parse_qs

async def bypass_tg_navigation(page):
    tg_target = {}
    async def intercept(route):
        url = route.request.url
        if 't.me/' in url or 'telegram.me/' in url:
            parsed = urlparse(url)
            path = parsed.path.strip('/')
            tg_target['username'] = path.split('/')[0] if path else None
            qs = parse_qs(parsed.query)
            tg_target['start_param'] = qs.get('start', qs.get('startapp', [None]))[0]
            await route.abort()
        else:
            await route.continue_()
    await page.route('**/*', intercept)
    return tg_target