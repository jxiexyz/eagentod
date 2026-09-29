# Origin Domain: nibblins.xyz (Generic Airdrop Portal)
# Date: 2026-08-26
# Symptom: Browser hangs on t.me/tg:// links or social popups during task execution.

import asyncio

async def bypass_social_redirects(page, verify_selector="button:has-text('Verify'), button:has-text('Check'), button:has-text('Submit')"):
    await page.evaluate('''() => {
        window.open = () => null;
        document.addEventListener('click', (e) => {
            const a = e.target.closest('a');
            if (a && (a.href.includes('t.me') || a.href.includes('twitter.com') || a.href.includes('x.com'))) {
                e.preventDefault();
                console.log('Blocked external link');
            }
        }, true);
    }''')
    try:
        buttons = await page.locator(verify_selector).all()
        for btn in buttons:
            if await btn.is_visible():
                await btn.click()
                await asyncio.sleep(2)
    except Exception:
        pass
