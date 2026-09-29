# Metadata: Origin Domain app.stabilizer.finance, Date 2026-08-23, Symptom: Wallet connection UI block/timeout on profile page.

import asyncio

async def inject_evm_wallet(page, wallet_address: str):
    """
    Injects a mock EIP-1193 provider to bypass UI wallet modals.
    """
    # ponytail: mocks eth_requestAccounts, add transaction signing when [minting requires actual signature propagation].
    mock_provider = f"""
    window.ethereum = {{
        isMetaMask: true,
        request: async (args) => {{
            if (args.method === 'eth_requestAccounts' || args.method === 'eth_accounts') return ['{wallet_address}'];
            if (args.method === 'eth_chainId') return '0x1';
            return null;
        }},
        on: () => {{}},
        removeListener: () => {{}}
    }};
    """
    await page.add_init_script(mock_provider)
    
    selectors = ['button:has-text("Connect Wallet")', 'button:has-text("Connect")', '[data-testid="connect-button"]']
    for selector in selectors:
        btns = await page.locator(selector).all()
        for btn in btns:
            if await btn.is_visible():
                await btn.click()
                await asyncio.sleep(1)
                return True
    return False
