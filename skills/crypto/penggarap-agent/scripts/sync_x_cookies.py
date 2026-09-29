#!/usr/bin/env python3
"""
Extract X/Twitter cookies from the active CDP browser and update the rettiwt-api key.
Useful when mcp_airdrop_tools_x_* returns 401 Unauthorized due to expired MCP cookies,
even when the CDP browser itself is still logged in.
"""
import asyncio, base64, os
from playwright.async_api import async_playwright

async def sync():
    async with async_playwright() as p:
        try:
            b = await p.chromium.connect_over_cdp('http://localhost:9222')
        except Exception as e:
            print(f"Failed to connect to CDP: {e}")
            return
        
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
            print('Failed to find auth_token or ct0. Is the browser logged into X.com?')

if __name__ == '__main__':
    asyncio.run(sync())
