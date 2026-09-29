# Metadata: ax1.vc, 2026-08-24, EVM Wallet connection failure on Base Sepolia

async def inject_mock_wallet(page, wallet_address: str, chain_id: str = "0x14a34"):
    """
    Injects an EIP-6963 and window.ethereum compatible mock provider.
    Defaults to Base Sepolia (0x14a34).
    """
    script = f"""
    (() => {{
        const provider = {{
            isMetaMask: true,
            request: async (args) => {{
                if (args.method === 'eth_requestAccounts' || args.method === 'eth_accounts') return ["{wallet_address}"];
                if (args.method === 'eth_chainId') return "{chain_id}";
                if (args.method === 'wallet_switchEthereumChain' || args.method === 'wallet_addEthereumChain') return null;
                if (args.method === 'personal_sign' || args.method === 'eth_signTypedData_v4') return "0xmocksignature";
                return null;
            }},
            on: (event, handler) => {{}},
            removeListener: (event, handler) => {{}},
        }};
        const event = new CustomEvent("eip6963:announceProvider", {{
            detail: {{
                info: {{
                    uuid: "mock-wallet-uuid",
                    name: "Hermes Mock Wallet",
                    icon: "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZD0iTTExIDEySDEzVjE0SDExVjEyWk0xMSAxNkgxM1YxOEgxMVYxNloiIGZpbGw9IiNmZmYiLz48L3N2Zz4=",
                    rdns: "io.hermes.mock"
                }},
                provider: provider
            }}
        }});
        window.addEventListener("eip6963:requestProvider", () => window.dispatchEvent(event));
        window.dispatchEvent(event);
        window.ethereum = provider;
    }})();
    """
    await page.add_init_script(script)
    await page.evaluate(script)
