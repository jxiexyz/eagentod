# Metadata: Origin Domain: ax1.vc, Date: 2026-08-24, Symptom: Standard locators fail on EVM wallet connect modals due to Shadow DOM (Dynamic.xyz/Privy).

async def bypass_wallet_connect(page, connect_selector="button:has-text('Connect Wallet')", wallet_name="MetaMask"):
    """
    Generic bypass for piercing shadow DOM wallet connect modals.
    """
    # Click the main connect button
    await page.locator(connect_selector).first.click(timeout=5000)
    
    # Attempt to pierce Dynamic.xyz shadow DOM first, fallback to generic text
    try:
        dynamic_locator = page.locator(f'.dynamic-shadow-dom >> text={wallet_name}')
        await dynamic_locator.first.click(timeout=5000)
    except:
        generic_locator = page.locator(f'text={wallet_name}')
        await generic_locator.first.click(timeout=5000)
    
    return True
