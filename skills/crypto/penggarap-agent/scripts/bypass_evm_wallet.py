# Metadata: Origin: ax1.vc | Date: 2026-08-24 | Symptom: Missing EVM wallet connection for Base Sepolia (84532)

async def bypass_evm_connection(page, target_address: str, chain_id: int = 84532):
    """Inject mock window.ethereum to bypass wallet connect overlays."""
    injection_script = f"""
        window.ethereum = {{
            isMetaMask: true,
            chainId: '0x{chain_id:x}',
            request: async (req) => {{
                if (req.method === 'eth_requestAccounts' || req.method === 'eth_accounts') return ['{target_address}'];
                if (req.method === 'eth_chainId') return '0x{chain_id:x}';
                if (req.method === 'wallet_switchEthereumChain' || req.method === 'wallet_addEthereumChain') return null;
                console.warn('Unmocked ETH method:', req.method);
                return null;
            }},
            on: () => {{}},
            removeListener: () => {{}}
        }};
    """
    await page.add_init_script(injection_script)
