# Fallback Strategy: lite_nav for CDP Tunnel Errors

When `browser_navigate` fails with `net::ERR_TUNNEL_CONNECTION_FAILED` (typically due to proxy or CDP supervisor issues on certain domains), DO NOT immediately skip the target.

**Bypass:**
1. Fallback to the lightweight browser: `mcp_airdrop_tools_lite_nav(url)`.
2. Use `mcp_airdrop_tools_lite_info()` to read the DOM state and visible buttons.
3. Proceed with the task using `mcp_airdrop_tools_lite_click(text)` and `mcp_airdrop_tools_lite_fill(selector, value)`.
4. Verify success via `mcp_airdrop_tools_lite_info()` before reporting ✅.
