# Metadata: Domain (s.kaito.ai), Date (2026-08-19), Symptom (hermes -z: no final response was produced / navigation hang)

async def route_abort_heavy_resources(route):
    blocked_domains = ['google-analytics.com', 'segment.com', 'mixpanel.com']
    if any(b in route.request.url for b in blocked_domains) or route.request.resource_type in ['image', 'media', 'font']:
        await route.abort()
    else:
        await route.continue_()

async def robust_goto(page, url, timeout=30000):
    await page.route('**/*', route_abort_heavy_resources)
    try:
        await page.goto(url, wait_until='domcontentloaded', timeout=timeout)
    except Exception as e:
        print(f'Navigation exception handled (bypassing hang): {e}')
