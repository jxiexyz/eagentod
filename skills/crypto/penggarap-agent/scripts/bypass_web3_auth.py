# Metadata: Origin Domain: app.rally.fun, Date: 2026-08-26, Symptom: Web3 auth modal overlay blocking wallet connection flow

async def bypass_web3_auth(page, wallet_regex="(?i)metamask|browser wallet"):
    await page.wait_for_load_state('domcontentloaded')
    for btn_text in ["Connect", "Login", "Sign In"]:
        try:
            await page.locator(f"button:has-text('{btn_text}')").first.click(timeout=1500)
        except: 
            pass
            
    await page.wait_for_timeout(1000)
    
    try:
        await page.locator(f"button >> text=/{wallet_regex}/").first.click(timeout=2000)
        return True
    except:
        return False
