# Metadata: Origin Domain: app.meridian.xyz, Date: 2026-08-22, Symptom: Fails to interact with web3 connect, predict, and faucet elements due to shadow DOM or overlay obstruction.

async def web3_predict_bypass(page, selectors: dict):
    """
    Generic JS-injected bypass for clicking obscured Web3 elements (connect, faucet, predict).
    Args:
        page: Playwright page object
        selectors (dict): Dictionary mapping steps to CSS selectors. 
                          e.g., {'connect': '#connect-btn', 'faucet': '.claim-testnet', 'predict': '.predict-btn'}
    """
    import asyncio
    
    for step, selector in selectors.items():
        try:
            # JS evaluation pierces certain overlays and shadow DOM boundaries better than standard locator clicks
            await page.evaluate(f'''(sel) => {{
                const el = document.querySelector(sel);
                if (el) {{
                    el.scrollIntoView({({behavior: 'smooth', block: 'center'})});
                    el.click();
                }}
            }}''', selector)
            await asyncio.sleep(3)  # Buffer for Web3 RPC response / UI transition
        except Exception as e:
            print(f"Bypass step '{step}' failed on selector '{selector}': {e}")
    
    return True
