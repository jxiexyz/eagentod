# Origin Domain: hub.axisrobotics.ai
# Date: 2026-08-26
# Symptom: Web3 wallet extension connection fails or hangs waiting for popup in headless automation.

async def inject_mock_wallet(page, provider_name="BinanceChain", wallet_address="0x444b38c15ccc46db22b9590497023d91e506b2ff", chain_id="0x38"):
    """
    Injects a mock Web3 wallet provider into the page to bypass extension connection popups and signature requests.
    """
    mock_script = f"""
        window.{provider_name} = {{
            isBinance: true,
            isMetaMask: true,
            request: async (args) => {{
                if (args.method === 'eth_requestAccounts' || args.method === 'eth_accounts') {{
                    return ['{wallet_address}'];
                }}
                if (args.method === 'eth_chainId') {{
                    return '{chain_id}';
                }}
                if (args.method === 'personal_sign' || args.method === 'eth_signTypedData_v4' || args.method === 'eth_sign') {{
                    return '0x' + '1'.repeat(130);
                }}
                if (args.method === 'eth_sendTransaction') {{
                    return '0x' + '2'.repeat(64);
                }}
                return null;
            }},
            on: () => {{}},
            removeListener: () => {{}}
        }};
    """
    await page.add_init_script(mock_script)
