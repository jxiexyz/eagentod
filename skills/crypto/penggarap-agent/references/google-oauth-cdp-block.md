# Playwright OAuth Multi-Tab Hanging Pitfall

## The Problem
When clicking "Connect Google" or "Connect X" on dApps, they open a popup window for OAuth.
If you use `browser_navigate` on the popup URL, the dApp's main page state resets, the `window.opener` context is destroyed, and the login silently fails after authorization.

Using a Playwright script to find the target tab and click "Authorize" works, but sometimes the script hangs, fails to find the button, or encounters a blocked Google OAuth screen because of Playwright's CDP fingerprint.

## Playwright Google OAuth CDP Block (The "Anti-Bot" Block)
If you attempt to authorize Google OAuth via Playwright/CDP and Google detects the automation, it throws the user to a manual email/password screen, dropping the auto-login session. 

**DO NOT** attempt to fill the email/password via Playwright if this happens.
**DO NOT** continue executing `browser_click` or CDP scripts on the blocked target. 

## The Solution

1. **Verify if it's a Hard Block:** 
   If `accounts.google.com` loads a manual email/password input instead of the "Continue as Momo" modal, it is a hard block.

2. **Abort CDP Execution:**
   Do not force Playwright to type the password. Exit the OAuth handler script immediately to prevent the account from being locked by Google.

3. **Manual VNC Intervention (One-Time):**
   - Connect via VNC.
   - Open `google.com` manually in the main Chrome window to verify the session.
   - If logged out, log in manually via VNC.
   - Return to the dApp tab (e.g., `link.kgen.io`) and click the Google OAuth button manually in the VNC session.
   - Click "Continue" manually on the Google popup.
   - Once the token is saved in the browser, the worker can resume automation.

4. **Fallback (If VNC is not possible immediately):**
   - Use `imap_reader.py` to login via Email OTP instead of Google OAuth if the dApp supports standard email login.
