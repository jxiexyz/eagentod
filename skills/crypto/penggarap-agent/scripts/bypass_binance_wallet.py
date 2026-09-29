# Metadata: Domain: hub.axisrobotics.ai, Date: 2026-08-26, Symptom: Binance Wallet Extension missing/unreachable in headless automation

async def bypass_binance_wallet(page, wallet_address='0x444b38c15ccc46db22b9590497023d91e506b2ff'):
    '''Injects mock Binance Wallet (window.BinanceChain) into the page environment.'''
    mock_script = f'''
        window.BinanceChain = {{
            isBinance: true,
            request: async (args) => {{
                if (args.method === "eth_requestAccounts" || args.method === "eth_accounts") {{
                    return ["{wallet_address}"];
                }}
                if (args.method === "eth_chainId") {{
                    return "0x38";
                }}
                if (args.method === "personal_sign" || args.method === "eth_signTypedData_v4") {{
                    return "0xmockedsignature00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";
                }}
                return null;
            }},
            on: () => {{}},
            removeListener: () => {{}}
        }};
        if (!window.ethereum) window.ethereum = window.BinanceChain;
    '''
    await page.add_init_script(mock_script)