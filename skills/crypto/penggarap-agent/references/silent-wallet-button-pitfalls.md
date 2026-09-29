# Silent Wallet Buttons & Dead Connect UI

**Symptom:**
You click "MetaMask", "WalletConnect", or "Connect" (or text like "Not linked yet") and absolutely nothing happens. The modal stays open, no loading spinner, no error. 
Attempting JS bypass (`universal_bypass.js`) or direct `.click()` via evaluate also does nothing.
Attempting to manually trigger `window.ethereum.request({ method: 'eth_requestAccounts' })` might execute successfully, but the site's UI doesn't acknowledge it or update its state.

**Root Cause:**
1. The site's frontend wallet connector (e.g., Wagmi, RainbowKit, AppKit) eagerly checks for specific provider flags (like `isMetaMask === true`) strictly at page load. If it doesn't find exactly what it wants, it binds an empty handler or silently disables the click event.
2. The UI element (e.g., "Not linked yet") might be purely presentational, and the actual connection flow is disabled until a prerequisite (like linking Discord/X first) is met, but the UI fails to communicate this.

**Worker Tactic:**
1. Ensure `wallet_connect.py --alive 1` (or `--ecosystem solana`) is injected.
2. Attempt direct JS click (e.g., `.click()` via XPath/evaluate).
3. Attempt explicit provider trigger: `window.ethereum.request({ method: "eth_requestAccounts" })`.
4. If all the above fail and the UI remains completely static (no loaders, no state changes, no errors), this is a **SOFT_BLOCK_EXHAUSTED**.
5. Stop wasting iterations. Report `❌ [domain] — mentok connect wallet, tombol/UI ga merespon meski udah di-bypass via JS.`