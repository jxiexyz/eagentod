# Origin Domain: app.stabilizer.finance
# Date: 2026-08-23
# Symptom: Profile connection / Wallet connect modal interaction fails due to shadow DOM or missing injected provider.

import asyncio
from playwright.async_api import Page

async def bypass(page: Page, connect_selector: str = "text=/connect|sign in|profile|wallet/i"):
    """
    Bypass web3 profile connection screens by forcefully injecting mock providers
    and piercing shadow DOMs to click the connect button.
    """
    # Inject standard window.ethereum mock if not present for wallet connect triggers
    await page.add_init_script("""
        if (!window.ethereum) {
            window.ethereum = {
                isMetaMask: true,
                request: async (args) => {
                    if (args.method === 'eth_requestAccounts') return ['0x444b38c15ccc46db22b9590497023d91e506b2ff'];
                    if (args.method === 'eth_chainId') return '0x2105'; // Base chain standard
                    return null;
                },
                on: () => {},
                removeListener: () => {},
                autoRefreshOnNetworkChange: false
            };
        }
    """)
    
    try:
        # Attempt to click connect using playwright's text selector which penetrates open shadow DOMs natively
        connect_btn = page.locator(connect_selector).first
        await connect_btn.wait_for(state="visible", timeout=5000)
        await connect_btn.click(force=True)
        
        # Wait for potential modal rendering
        await page.wait_for_timeout(2000)
        
        # Auto-trigger wallet request to simulate successful click response
        await page.evaluate("window.ethereum.request({method: 'eth_requestAccounts'})")
        return True
    except Exception as e:
        print(f"Bypass profile connect failed: {e}")
        return False
