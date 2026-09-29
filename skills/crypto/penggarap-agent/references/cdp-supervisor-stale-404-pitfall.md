# CDP Supervisor Stale 404 Pitfall

**Symptom:**
You encounter `ECONNREFUSED 127.0.0.1:9222` during browser actions, indicating the headless Chromium process has crashed. You attempt to recover by running `pkill -f chrome` followed by restarting the browser in the terminal (`chromium-browser --headless=new ...`).
However, subsequent calls to `browser_navigate` or `mcp_airdrop_tools_lite_nav` fail with `CDP WebSocket connect failed: HTTP error: 404 Not Found` or `Target page, context or browser has been closed`.

**Root Cause:**
The Hermes tools (`browser_navigate`, `lite_nav`) rely on a persistent Playwright/CDP supervisor that maintains internal connection pools and target caches. When you manually kill and restart the underlying browser process, the supervisor's state becomes out of sync with the new browser's CDP targets, causing immediate 404s.

**Resolution / Rule:**
- **DO NOT** attempt to manually restart the Chromium process mid-execution using terminal commands.
- If a hard crash (`ECONNREFUSED`) occurs and persists, immediately report the task as `❌ [Domain] — CDP Crash` with category `SOFT_BLOCK_EXHAUSTED`.
- Allow the current worker run to fail gracefully so the external cron environment can perform a clean teardown and reset of both the browser and the CDP supervisor before the next cycle.