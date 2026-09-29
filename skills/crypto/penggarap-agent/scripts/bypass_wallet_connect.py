# Metadata: Origin: hub.axisrobotics.ai | Date: 2026-08-27 | Symptom: Binance Wallet Extension connection block and shadow DOM isolation
import asyncio

async def bypass_wallet_connect(page, selector, provider_key='BinanceChain'):
    await page.wait_for_load_state('domcontentloaded')
    try:
        await page.wait_for_function(f'window.{provider_key} !== undefined', timeout=3000)
    except:
        pass
    try:
        await page.click(selector, timeout=3000)
    except:
        await page.evaluate('''((sel) => {
            const findDeep = (root, s) => {
                if (root.querySelector(s)) return root.querySelector(s);
                for (const el of root.querySelectorAll('*')) {
                    if (el.shadowRoot) {
                        const found = findDeep(el.shadowRoot, s);
                        if (found) return found;
                    }
                }
                return null;
            };
            const btn = findDeep(document, sel);
            if (btn) btn.click();
        })''', selector)
    await asyncio.sleep(2)