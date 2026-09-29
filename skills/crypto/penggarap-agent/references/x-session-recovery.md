# X Session Recovery Procedure

When X/Twitter session is expired in the CDP browser (port 9222), follow this procedure.

## Detection
Navigate to `https://x.com/home`. If snapshot shows "Log in" instead of timeline → session expired.

## Recovery: Cookie Injection (Preferred)
Inject cookies from the saved file — faster and more reliable than login form.

```bash
python3 /home/ubuntu/.hermes/scripts/inject_x_cookies.py
```

If the script doesn't exist, create it or run inline:
```bash
python3 -c "
import json, asyncio
from playwright.async_api import async_playwright
async def inject():
    with open('/home/ubuntu/.hermes/x_cookies.json') as f:
        cookies = json.load(f)
    formatted = []
    for c in cookies:
        fc = {'name': c['name'], 'value': c['value'], 'domain': c['domain'],
              'path': c['path'], 'secure': c['secure'], 'httpOnly': c['httpOnly'],
              'expires': c['expirationDate']}
        if 'sameSite' in c:
            sm = c['sameSite']
            fc['sameSite'] = 'None' if sm == 'no_restriction' else sm.capitalize()
        formatted.append(fc)
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = browser.contexts[0]
        await ctx.add_cookies(formatted)
        page = await ctx.new_page()
        await page.goto('https://x.com/home')
        await asyncio.sleep(3)
        title = await page.title()
        await page.close()
        print(f'Result: {title}')
asyncio.run(inject())
"
```

**Success:** Title = "Beranda / X" or "Home / X"
**Failure:** Title = "X" or "Log in" → cookies expired, need manual login via VNC.

## Recovery: Login Form (Fallback)
If cookies are expired too:
1. Navigate to `https://x.com/login`
2. Fill `input[name="username_or_email"]` with `chiquast`
3. Fill `input[type="password"]` with password from `airdrop_identity.py`
4. Submit via `form.requestSubmit()` (button may not be inside `<form>`)
5. Check for rate limit: `document.querySelectorAll('[role="alert"]')` → "temporarily limited" = HARD BLOCK

## Rate Limit Response
If X says "We've temporarily limited your login":
- This is a HARD BLOCK. No workaround.
- Report ❌ for ALL X-dependent tasks this cycle with "X login rate limited, nunggu"
- Do NOT retry login — it makes the rate limit worse.
- X-dependent tasks: any site with "Connect X", "Sign in with X", X OAuth redirect.
