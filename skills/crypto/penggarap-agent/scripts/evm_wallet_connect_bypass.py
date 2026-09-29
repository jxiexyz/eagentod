# Origin Domain: platypusinc.cash
# Date: 2026-08-24
# Specific Symptom: EVM wallet connection failure in headless browser missing EIP-6963

async def inject_wallet_provider(page, wallet_address, chain_id="0x14a34"):
    await page.add_init_script(f"""
        window.ethereum = {{
            isMetaMask: true,
            request: async (req) => {{
                if (req.method === 'eth_requestAccounts' || req.method === 'eth_accounts') return ['{wallet_address}'];
                if (req.method === 'eth_chainId') return '{chain_id}';
                return null;
            }},
            on: () => {{}},
            removeListener: () => {{}}
        }};
        window.dispatchEvent(new CustomEvent('eip6963:announceProvider', {{
            detail: {{ info: {{ uuid: crypto.randomUUID(), name: 'InjectedWallet', rdns: 'io.metamask' }}, provider: window.ethereum }}
        }}));
    """)