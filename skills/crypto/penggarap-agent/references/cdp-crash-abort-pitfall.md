# Pitfall: CDP Browser Context Closed / Crash

**Symptom:** 
`ERROR: Page.goto: Target page, context or browser has been closed` (from `lite_nav` or `browser_navigate`).

**CRITICAL RULE:**
This is an INFRASTRUCTURE failure, not a target failure. The browser crashed or the CDP connection dropped. 
**DO NOT REPORT ❌ TO TOPIC 42.** If you report this as ❌, you are giving a false negative (claiming the site is dead when it's actually our browser that died), which ruins the airdrop pipeline.

**Action to Take:**
1. **DO NOT** call `post_topic42.py ❌`.
2. **DO NOT** mark the target as failed.
3. You MUST ABORT the current target and STOP execution entirely, or successfully restart the browser before continuing.
4. If you cannot recover the browser via known troubleshooting steps (e.g., reading `references/cdp-chromium-troubleshooting.md`), simply stop processing further targets and return a final message stating the infrastructure crashed. The cron job will retry the remaining targets on its next run.