### CDP Browser Pitfalls

**1. `Runtime.evaluate` `removeAttribute('disabled')` failure**
- **Symptom**: `browser_cdp` call with `method='Runtime.evaluate'` and `expression='document.querySelector("selector").removeAttribute("disabled")'` fails with error: `'Runtime.evaluate' wasn't found`.
- **Cause**: This seems to be an intermittent issue with the `browser_cdp` tool's interaction with the CDP `Runtime.evaluate` method or the way the Python client wrapper handles it. It does not consistently mean the browser is unhealthy.
- **Workaround**: If `browser_cdp` fails with this specific error when trying to remove a `disabled` attribute, consider the element effectively un-interactable via direct JS manipulation through `browser_cdp` for that specific attempt. Revert to waiting for the element to become enabled naturally, or escalate if the task is blocked.

**2. `CDP WebSocket connect failed: IO error: Connection refused`**
- **Symptom**: `browser_navigate` or any `browser_` tool fails with `CDP WebSocket connect failed: IO error: Connection refused`.
- **Cause**: The local Chromium instance (CDP port 9222) has either crashed, frozen, or is no longer reachable. This is a fatal error for web-based automation tasks in the current run.
- **Action**: When this error occurs, it indicates a complete breakdown of the browser environment. All subsequent web-based airdrop tasks in the current batch MUST be skipped and reported as failed. The system requires a restart or manual intervention to re-establish the Chromium connection.
