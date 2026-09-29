# Metadata: Domain: thor.savethelife.io, Date: 2026-08-25, Symptom: Social tasks open new tabs and disrupt signup flow
async def bypass_social_tasks(page, wallet_address):
    """
    Bypasses forced social tasks (Twitter/TG) by preventing new tabs
    and simulating clicks, then fills the wallet address.
    """
    await page.evaluate('''() => {
        window.open = () => null;
        document.querySelectorAll('a[target="_blank"]').forEach(a => a.removeAttribute('target'));
    }''')
    
    elements = await page.locator("a, button").all()
    for el in elements:
        try:
            text = (await el.inner_text()).lower()
            if any(k in text for k in ['twitter', 'telegram', 'follow', 'join', 'verify']):
                await el.click(force=True)
                await page.wait_for_timeout(1000)
        except Exception:
            continue
            
    inputs = await page.locator("input").all()
    for inp in inputs:
        try:
            placeholder = (await inp.get_attribute("placeholder") or "").lower()
            if any(k in placeholder for k in ["address", "bsc", "wallet", "bep20", "0x"]):
                await inp.fill(wallet_address, force=True)
        except Exception:
            continue
            
    for el in elements:
        try:
            text = (await el.inner_text()).lower()
            if any(k in text for k in ['submit', 'sign up', 'register', 'claim']):
                await el.click(force=True)
                await page.wait_for_timeout(2000)
        except Exception:
            continue