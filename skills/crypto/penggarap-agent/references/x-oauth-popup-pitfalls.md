# X.com OAuth Popup Pitfalls (Session Expiry & Silent Fails)

When navigating to X.com OAuth pages (e.g., `x.com/i/oauth2/authorize`), the worker often encounters silent failures where the "Authorize app" button is missing because the underlying CDP browser session has quietly expired.

## Symptoms
1. You navigate to `https://x.com/i/oauth2/authorize?...`
2. `browser_snapshot` shows no "Authorize app" button.
3. It only shows generic X login links:
   ```
   - link "Log in" [ref=e3]
   - link "help center" [ref=e2]
   ```
4. A direct `page.content()` or `document.body.innerText` reveals:
   `"To use this App you have to be logged in to X. Log in Learn more about 3rd party app access in the help center."`

## The Pitfall
The CDP browser (port 9222) is *supposed* to be persistently logged into X.com. However, Twitter/X frequently expires active sessions for security reasons (or due to headless fingerprinting).

When this happens, the OAuth redirect drops you onto an unauthenticated page that prompts you to log in manually. 

## The Resolution: Auto-Login Recovery

Unlike previously assumed, **the worker CAN and MUST attempt to recover the session** if credentials are provided in `airdrop_identity.py`. 

When the session is expired (Knowledge Check / Anti-Bot blocks the OAuth flow):
1. **DO NOT try to fill the login form inside the popup/OAuth frame.** X's Anti-Bot will often block popup-based logins with a "Knowledge Check" loop (`#/s/knowledge_check/...`).
2. **Close all tabs except one.**
3. Create a clean page: `await context.new_page()`
4. Navigate explicitly to `https://x.com/login`.
   - *CRITICAL TIMEOUT PITFALL:* DO NOT use `await page.wait_for_load_state("networkidle")` after navigating to X.com. Background polling will frequently cause a 30s timeout and crash the script. Use `await page.wait_for_load_state("domcontentloaded")` or wait for the input selector instead.
5. Use Playwright to fill the login flow (username -> password). 
   - *CRITICAL:* Always use Playwright's native `page.fill()` and `page.click()` to mimic human interaction. Avoid injecting JS directly on the login form to reduce bot-detection triggers.
   - *CRITICAL (August 2026 X DOM Changes):* 
     - **New Combined Login Form:** X now shows username AND password fields in the SAME dialog form. Fill both before submitting.
     - **Username Input:** Find by `input[name="username_or_email"]` — there are TWO duplicate forms on the page. Use the one inside the dialog (the overlay, not the background form).
     - **Password Input:** Find by `input[name="password"]` or `input[type="password"]` in the same form.
     - **Continue Button:** The "Continue" button may NOT be inside the `<form>` tag. It's a sibling element. Use `form.requestSubmit()` or find the button by walking up the DOM tree.
     - **Rate Limiting:** X will respond with `"We've temporarily limited your login. Please try again later."` after too many automated login attempts. This is a HARD BLOCK — no workaround. Report failure and wait. Check for this error via `document.querySelectorAll('[role="alert"]')`.
     - **Security Checks:** If X prompts for email, parse it from `airdrop_identity.py` (using `ast.parse` to extract the `IDENTITY` dict without executing the file) and fill it. If X presents a phone verification loop hardcoded to a US `+1` country code, the account is temporarily hard-blocked. Report the failure and abort.
6. **Wait for the auth_token cookie to be set:** Check `context.cookies('https://x.com')` for `auth_token`.
7. Once `auth_token` is present, the session is recovered. Retry the original target site (Rally, Takeapeak, etc.) — the OAuth flow will now work automatically.

### X Session Recovery via MCP (Preferred for Worker Agent)
**CRITICAL PITFALL: NEVER use `mcp_airdrop_tools_lite_nav` for X.com (OAuth, login, or home).** The lightweight browser (`lite_nav`) does NOT share the CDP port 9222 profile/cookies where `@chiquast` is authenticated, so X.com will always appear logged out in `lite_nav`. Always use CDP port 9222 (`browser_navigate` or Playwright CDP connection) for X.com.

When using Hermes browser tools (not standalone Playwright):
1. Check if X session is alive: `browser_navigate("https://x.com/home")` (over CDP port 9222) → if snapshot shows "Log in" instead of timeline → session expired.
2. Navigate to `https://x.com/login`, wait 3s for form to load.
3. Find username input: `browser_type` into the `input[name="username_or_email"]` field.
4. Password field should be on same form — use `browser_console` with React native setter to fill it.
5. Submit via `form.requestSubmit()` in `browser_console`.
6. **Check for rate limit:** `document.querySelectorAll('[role="alert"]')` — if "temporarily limited", STOP and report ❌ with "X login rate limited, perlu nunggu".
7. If login succeeds, verify `auth_token` cookie exists, then retry the original target.

If the automated login gets irrevocably stuck (e.g. requires 2FA or captcha the agent cannot solve), THEN fail the task and request human intervention. But always attempt the automated login recovery first.