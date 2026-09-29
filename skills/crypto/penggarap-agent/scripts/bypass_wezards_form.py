# Metadata: wezards.xyz, 2026-08-20, Custom script to handle Math Captcha and dispatchEvent('change') on React inputs
import asyncio
from playwright.async_api import async_playwright

async def run(page_url, username, reply_url, wallet):
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp('http://localhost:9222')
        context = browser.contexts[0]
        page = None
        for pg in context.pages:
            if 'wezards' in pg.url:
                page = pg
                break
        if not page:
            page = await context.new_page()
            await page.goto(page_url)
        
        # Follow X accounts in separate tabs
        for acc in ['We_Zards', 'SickickZards']:
            px = await context.new_page()
            try:
                await px.goto(f'https://x.com/{acc}', wait_until='domcontentloaded', timeout=15000)
                await asyncio.sleep(2)
                btn = await px.query_selector('[data-testid$="-follow"]')
                if btn: await btn.click()
                await asyncio.sleep(1)
            except Exception:
                pass
            finally:
                await px.close()
        
        await page.bring_to_front()
        
        # Solve Math CAPTCHA
        captcha_info = await page.evaluate('''() => {
            const match = document.body.innerText.match(/(\d+)\s*([\+\-\*])\s*(\d+)\s*=\s*\?/);
            if (match) {
                const [_, n1, op, n2] = match;
                return eval(`${n1}${op}${n2}`);
            }
            return null;
        }''')
        if not captcha_info: return False

        # Fill form
        inputs = await page.query_selector_all('input')
        values = [username, reply_url, wallet, str(captcha_info)]
        for i, val in enumerate(values):
            if i < len(inputs):
                await inputs[i].fill(val)
                await inputs[i].dispatch_event('input')
                await inputs[i].dispatch_event('change')
        
        await asyncio.sleep(1)
        submit = await page.query_selector('button[type="submit"]')
        await submit.click()
        await asyncio.sleep(3)
        
        return 'ENTRY RECORDED' in await page.evaluate('() => document.body.innerText')

# Call run() with your args