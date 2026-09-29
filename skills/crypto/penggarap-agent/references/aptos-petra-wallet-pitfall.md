# Aptos / Petra Wallet Pitfall

**Issue:**
A target site (e.g., `portal.rhuna.io`) blocks the main UI with a "Petra Wallet Required" modal or strictly requires an Aptos wallet connection.

**Why it fails:**
Our `wallet_connect.py` script injects mock objects for EVM (`window.ethereum`) and Solana (`window.phantom.solana`). It does **not** mock Aptos (`window.aptos`).

**Detection:**
1. A dialog/modal specifically asks to "Install Petra Wallet" or connects to Aptos.
2. Check console: `browser_console(expression="window.aptos ? 'present' : 'missing'")` returns missing.

**Action:**
This is a Hard-Block. Immediately stop execution for this site.
Report failure in Telegram (e.g., `❌ [domain] — mentok butuh Petra wallet (Aptos), ga bisa pake EVM/Solana biasa.`).
