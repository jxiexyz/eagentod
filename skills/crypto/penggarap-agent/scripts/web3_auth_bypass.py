# Metadata: Domain: app.rally.fun, Date: 2026-08-26, Symptom: Web3 Auth connection failure/modal block
import asyncio

async def handle_wallet_connect(page, wallet_name='MetaMask'):
    """
    Handles generic Web3 auth modals piercing shadow DOMs if needed.
    """
    selectors = [
        f"button:has-text('{wallet_name}')",
        f"div[role='button']:has-text('{wallet_name}')",
        "button:has-text('Browser Wallet')",
        "text='Injected'"
    ]
    
    for sel in selectors:
        try:
            await page.wait_for_selector(sel, state='attached', timeout=2000)
            await page.click(sel, force=True)
            await asyncio.sleep(2)
            return True
        except Exception:
            pass
            
    # Shadow DOM fallback
    await page.evaluate('''(name) => {
        const walk = (root) => {
            for (const el of root.querySelectorAll('button, div[role="button"], li')) {
                if (el.textContent?.trim().includes(name) || el.textContent?.trim().includes('Browser Wallet')) {
                    el.click();
                    return true;
                }
            }
            for (const el of root.querySelectorAll('*')) {
                if (el.shadowRoot && walk(el.shadowRoot)) return true;
            }
            return false;
        };
        walk(document);
    }''', wallet_name)
    await asyncio.sleep(2)
    return True