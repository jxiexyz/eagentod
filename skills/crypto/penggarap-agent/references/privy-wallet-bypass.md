# Privy & Dynamic SDK Wallet Connect (Shadow DOM) Bypass

## The Challenge
Modern web3 dApps (e.g., BuilderFi, Perceptron) use Privy or Dynamic.xyz SDKs. These SDKs present significant automation challenges for headless browsers (Puppeteer/Playwright):
1.  **Shadow DOM:** Wallet selection buttons are hidden inside shadow roots (`dynamic-shadow-dom-content`), making them invisible to standard DOM selectors.
2.  **EIP-6963 Strict Checks:** Simple `window.ethereum = {}` injections are no longer sufficient. Privy validates wallet extensions against the EIP-6963 standard and will fallback to a WalletConnect QR Code (un-automatable) if it deems the injection "fake".
3.  **Cloudflare Turnstile:** The Privy iframe often enforces Cloudflare Turnstile CAPTCHAs, which endlessly loop "Verifying you are human" when they detect headless CDP connections without residential proxies.

## Bypass Strategies

### 1. The Google OAuth Bypass (Preferred for Privy)
When a site uses Privy, it almost always offers "Sign in with Email" or "Sign in with Google" alongside "Continue with Wallet".
-   **Why it works:** Privy creates an Embedded Wallet automatically when a user signs in via OAuth.
-   **Execution:** Instead of fighting the WalletConnect QR code, instruct the agent to click `Sign in with Google`. Since the CDP Chromium browser (port 9222) is already authenticated with Google, the OAuth flow bypasses Turnstile and WalletConnect entirely.

### 2. Full EIP-6963 Mock Provider (If Wallet is Mandatory)
If the site strictly requires an EVM wallet connection and forces the WalletConnect QR code fallback, the injection script must be upgraded to fully mock EIP-6963.

The injection script (`inject_wallet.js`) must emit the `eip6963:announceProvider` event and provide a comprehensive provider object containing `eth_requestAccounts`, `eth_chainId`, `personal_sign`, and `isConnected`.

*See `references/dynamic-wallet-connect.md` or `crypto-airdrop-ops/scripts/wallet_injector.py` for full mock payload implementation details.*

### 3. Graceful Failure
If a site strictly uses WalletConnect (no OAuth alternative) and the EIP-6963 mock fails (site still shows a QR code demanding a mobile device scan), the agent should gracefully fail (`❌ Failed - Membutuhkan scan code`) and **close the tab immediately** to prevent memory leaks. Do not attempt to parse the QR code.