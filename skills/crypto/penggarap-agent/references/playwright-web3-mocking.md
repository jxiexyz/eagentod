# Playwright Web3 Mocking (MetaMask Injection)

When an airdrop site requires clicking a "Connect Wallet" button (like MetaMask) and standard CDP execution cannot interact with browser extensions, you can inject a mock `window.ethereum` provider using Playwright's `add_init_script` BEFORE interacting with the button.

This forces the dApp to believe MetaMask is installed and instantly returns the provided EVM address when `eth_requestAccounts` is called.

## Python Playwright Implementation

```python
import asyncio
from playwright.async_api import async_playwright

async def run_mock_wallet(evm_address):
    async with async_playwright() as p:
        # Connect to existing CDP session
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        ctx = browser.contexts[0]
        page = ctx.pages[0]
        
        # Inject Web3 Mock globally before next interactions
        await page.add_init_script(f"""
            window.ethereum = {{
                isMetaMask: true,
                request: async (request) => {{
                    console.log("Mock ethereum request:", request.method);
                    if (request.method === 'eth_requestAccounts' || request.method === 'eth_accounts') {{
                        return ['{evm_address}'];
                    }}
                    if (request.method === 'eth_chainId') {{
                        return '0x1'; // Mainnet (or change to required chain)
                    }}
                    return null;
                }},
                on: (eventName, callback) => {{}},
                removeListener: (eventName, callback) => {{}}
            }};
        """)
        
        # Now click the connect button on the dApp
        # connect_btn = page.locator('button:has-text("MetaMask")')
        # if await connect_btn.count() > 0:
        #     await connect_btn.click()
```

## Bonus: Intercepting window.open
If a connect or social button aggressively opens new tabs (e.g., for X oauth or external wallets) and you need to prevent it to keep the React state contained in the current tab, inject an override:

```python
await page.evaluate('''
    window.open = function() {
        console.log("window.open intercepted");
        return null;
    };
''')
```