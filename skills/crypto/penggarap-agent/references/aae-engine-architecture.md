# Agentic Wallet Injector & Shadow DOM Airdrop Engine

During session on 2026-07-14, the user decided that "prompt-only" airdrop cron-jobs executed by `gemini-2.5-flash` were failing too frequently on modern Web3 sites (BuilderFi, Kalshi) due to:
1. Invisible Captchas (hCaptcha) blocking `browser_click`.
2. Dynamic.xyz / Shadow DOM Wallet Modals requiring injected providers *before* page load.
3. LLM "Hallucination" (claiming a task was completed just because it clicked "Login" or skipping tasks because it confused a URL domain with a previous failure).

To fix this, a hybrid approach (The Antigravity Airdrop Engine - AAE) was initiated. 
This bypasses prompt-driven unreliability by executing a strict Python script loop leveraging Playwright directly.

## AAE Architecture (`~/.hermes/scripts/aae/`)
- `aae_core.py` (Main Loop)
- `aae_wallet.py` (Robust Injector)
- `aae_social.py` (Twitter/X Native API tools wrapper to bypass MCP Shadowbans)

### The Robust Injector (aae_wallet.py)
A standard `{ isMetaMask: true }` inject via `browser_cdp` -> `Runtime.evaluate` often fails because it executes *after* the page loads, triggering fallback WalletConnect QR codes.
The AAE uses Playwright's `page.add_init_script` to ensure the mock `window.ethereum` and `window.solana` objects (containing full methods like `eth_requestAccounts`, `eth_chainId`, `personal_sign`) exist before the site's JS evaluates.

### Message ID De-Duplication
When reading links from Telegram (Topic 31), if multiple distinct messages contain the same domain (e.g. `form.typeform.com`), the prompt-only worker overwrites or skips them based purely on domain name.
**Fix:** Append the Telegram Message ID to the project name in `worker_done.json` (e.g., `form.typeform.com (Msg 294)`).

### MCP X Action Quirks
- The MCP tool `mcp_airdrop_tools_x_action` (used for follow/like) often returns `403 TWITTER_ERROR` (Cannot find specified user) when hitting accounts not in the local shadow-ban/API cache.
- **Fix:** If the API fails, fallback to native CDP browser manipulation or manual logging. (Prompt updated to mandate real social interaction before submitting forms).

### Strict Anti-Hallucination Policy
The worker's prompt (`penggarap-agent`) must enforce:
> JIKA BARU MENEKAN LOGIN / CONNECT WALLET / ENTER, ITU BELUM COMPLETED. HARAM MELAPORKAN COMPLETED SEBELUM MENCAPAI HALAMAN SUKSES/AKHIR. 
> JANGAN PERNAH BERBOHONG. Laporkan alasan konkrit (misal: "Isi email X, lalu klik submit").