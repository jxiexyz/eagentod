# Refreshing X API Session Cookies from CDP Browser

When `mcp_airdrop_tools_x_action` or `x_research.py` fails with HTTP 401 (Session Expired), the X cookies in `~/.hermes/.env_rettiwt` need to be regenerated. The CDP browser (port 9222) is usually still logged in, but the headless tools (`x_native.py` / `x_research.py`) use the saved cookie string.

The API key in `.env_rettiwt` is a base64 encoded string containing the raw cookie values: `twid=...;auth_token=...;ct0=...`. Both `x_native.py` and MCP tools read this file directly.

**Python Script to Extract and Refresh (Run via terminal):**

```python
import asyncio, base64, os
from playwright.async_api import async_playwright

async def sync_x_cookies():
    async with async_playwright() as p:
        b = await p.chromium.connect_over_cdp('http://localhost:9222')
        ctx = b.contexts[0]
        cookies = await ctx.cookies('https://x.com')
        
        twid = next((c['value'] for c in cookies if c['name'] == 'twid'), '')
        auth = next((c['value'] for c in cookies if c['name'] == 'auth_token'), '')
        ct0 = next((c['value'] for c in cookies if c['name'] == 'ct0'), '')
        
        if auth and ct0:
            cookie_str = f'twid={twid};auth_token={auth};ct0={ct0}'
            key = base64.b64encode(cookie_str.encode()).decode()
            
            env_path = os.path.expanduser('~/.hermes/.env_rettiwt')
            with open(env_path, 'w') as f:
                f.write(f'RETTIWT_API_KEY={key}\nAPI_KEY={key}\n')
            print(f'Successfully updated {env_path}')
        else:
            print('Missing auth_token or ct0. CDP browser needs manual X login.')

asyncio.run(sync_x_cookies())
```

Run this script to immediately restore social task capabilities for the agent. Verify with `python3 ~/.hermes/scripts/x_native.py whoami`.