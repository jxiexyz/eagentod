# Metadata: ax1.vc, 2026-08-24, EVM Wallet Connection Blocked / Missing window.ethereum

async def inject_mock_wallet(page, address: str = "0x444b38c15ccc46db22b9590497023d91e506b2ff", chain_id: str = "0x14a34"):
    """
    Injects a mock EIP-1193 / EIP-6963 provider into the page before load.
    chain_id defaults to Base Sepolia (84532 -> 0x14a34).
    """
    mock_script = f"""
    () => {{
        window.ethereum = {{
            isMetaMask: true,
            request: async (request) => {{
                if (request.method === 'eth_requestAccounts' || request.method === 'eth_accounts') {{
                    return ['{address}'];
                }}
                if (request.method === 'eth_chainId') {{
                    return '{chain_id}';
                }}
                if (request.method === 'wallet_switchEthereumChain' || request.method === 'wallet_addEthereumChain') {{
                    return null;
                }}
                if (request.method === 'personal_sign' || request.method === 'eth_signTypedData_v4') {{
                    return '0xmocksignature';
                }}
                if (request.method === 'eth_sendTransaction') {{
                    return '0xmocktxhash';
                }}
                throw new Error("Method not mocked: " + request.method);
            }},
            on: (eventName, callback) => {{}},
            removeListener: (eventName, callback) => {{}}
        }};
        
        const providerInfo = {{
            uuid: crypto.randomUUID(),
            name: 'Mock Wallet',
            icon: 'data:image/svg+xml,<svg></svg>',
            rdns: 'io.metamask'
        }};
        
        const announceEvent = new CustomEvent('eip6963:announceProvider', {{
            detail: Object.freeze({{ info: providerInfo, provider: window.ethereum }})
        }});
        
        window.dispatchEvent(announceEvent);
        window.addEventListener('eip6963:requestProvider', () => {{
            window.dispatchEvent(announceEvent);
        }});
    }}
    """
    await page.add_init_script(mock_script)
    return True
