# Phantom Wallet Mock Architecture (Solana)

To bypass Solana wallet connection prompts (like Phantom) in headless CDP browsers, we inject a mock `window.phantom.solana` object using the `wallet_connect.py` supervisor.

## How It Works
1. **Injection:** The script evaluates an IIFE in the target page that creates `window.phantom = { solana: { ... } }`.
2. **Properties:** Sets `isPhantom: true` and a `publicKey` object with `toString()` and `toBase58()` methods derived from the local identity file.
3. **Event Dispatch:** Dispatches `phantom#initialized` so the dApp (e.g., `@solana/wallet-adapter`) detects the wallet immediately without requiring a page reload.
4. **Sign Interception:** Overrides `connect()`, `signMessage()`, and `signTransaction()`. 
   - In `--mock-only` mode, it immediately returns dummy byte arrays (`new Uint8Array(64)`) to satisfy basic frontend validation.
   - In `--alive N` mode, it pushes the payload to `window.__wc_q` which the Python CDP supervisor polls, signs with `pynacl`/`base58` using the real private key, and returns asynchronously.

## Usage
```bash
python3 ~/.hermes/scripts/wallet_connect.py --url "DOMAIN" --ecosystem solana --mock-only
```
*Use this when standard EVM mocks (EIP-6963) fail to trigger connection modals on Solana-centric dApps (like voice.fun).*