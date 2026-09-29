# X.com Cookie Injection for CDP 9222

When the active CDP 9222 browser loses its X.com (Twitter) session or when navigating to `https://x.com/login` gets stuck (such as the form failing, or OAuth intercept iframes stealing focus like in Luckycall), **DO NOT use browser_navigate and browser_type to fill the login form again**. It is unreliable and often hits bot protections.

Instead, inject the known good session cookies directly into the browser context.

### The Source Cookies
The user's persistent X cookies are stored at `/home/ubuntu/.hermes/x_cookies.json`.

### The Injection Script
Save this script to `/tmp/inject_x_cookies.py` and run it via `terminal(command="python3 /tmp/inject_x_cookies.py")`.

```python
import json
import asyncio
from playwright.async_api import async_playwright

async def inject():
    with open('/home/ubuntu/.hermes/x_cookies.json', 'r') as f:
        cookies = json.load(f)
    
    formatted_cookies = []
    for c in cookies:
        fc = {
            'name': c['name'],
            'value': c['value'],
            'domain': c['domain'],
            'path': c['path'],
            'secure': c['secure'],
            'httpOnly': c['httpOnly'],
            'expires': c['expirationDate']
        }
        if 'sameSite' in c:
            if c['sameSite'] == 'no_restriction':
                fc['sameSite'] = 'None'
            elif c['sameSite'] == 'lax':
                fc['sameSite'] = 'Lax'
            elif c['sameSite'] == 'strict':
                fc['sameSite'] = 'Strict'
        formatted_cookies.append(fc)
    
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        await context.add_cookies(formatted_cookies)
        print("X cookies injected successfully!")

        page = await context.new_page()
        await page.goto("https://x.com/")
        try:
            # networkidle might timeout if background trackers hang
            await page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        print("X login state title:", await page.title())
        await page.close()

if __name__ == '__main__':
    asyncio.run(inject())
```

### Verification
If injection succeeded, the output will show `X login state title: Beranda / X` or `Home / X`. If it shows `Log in` or `Explore`, the cookies in the JSON file might be expired and need manual updating by the user.