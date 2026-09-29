# CDP Lite Nav Error: Context Closed (False Positive Dead Site)

**Issue**: During recon, `mcp_airdrop_tools_lite_nav` or standard browser tools return:
`ERROR: Page.goto: Target page, context or browser has been closed`

**Root Cause**: This is NOT a dead site (404/502). The underlying Playwright CDP connection (port 9222) crashed, died, or was closed externally.

**Worker Pitfall**: Do NOT report this as `❌ situs error pas direcon, ga bisa diload` or `situs mati`. This is an infrastructure failure, not a target failure. If you skip it as a dead site, the target is incorrectly marked as done.

**Resolution**:
1. Do not report `❌`.
2. Do not mark it done unless it's genuinely a bad URL.
3. If you must report it, state explicitly that the CDP browser crashed.
4. Review `references/cdp-chromium-troubleshooting.md` to restart or repair the CDP session before continuing.