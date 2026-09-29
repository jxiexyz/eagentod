# Gleam.io OAuth & Interaction Pitfalls

When automating campaigns on Gleam.io (e.g. `gleam.io/xxxx/campaign-name`), social login and entry verification have unique Angular 1.x and popup patterns.

## Symptoms
1. Clicking login icons (Twitter, Discord, Google) via `browser_click` navigates away or fails silently.
2. Clicking via JS (`document.querySelector('a.twitter-login').click()`) does not trigger the OAuth popup.
3. Polling `context.pages` after a sleep misses the popup because headless Chromium suppresses untracked `window.open()` calls.

## Root Cause
- Gleam uses AngularJS 1.x with event handlers bound via `ng-click="loginTwitter()"` or data attributes (`data-track-event`).
- The login buttons open popup windows using `window.open`. In Playwright/CDP, if you do not attach a popup listener (`page.expect_popup()` or `page.on('popup')`) *before* triggering the click, the popup may be blocked or closed prematurely by Chromium.

## Tactic / Resolution
1. **Use `expect_popup` context manager in Playwright:**
   ```python
   async with page.expect_popup() as popup_info:
       # Click the Gleam Twitter login button
       await page.locator('a.twitter-login, a[ng-click*="Twitter"]').click()
   popup = await popup_info.value
   await popup.wait_for_load_state("domcontentloaded")
   # Authorize app
   btn = popup.locator('button:has-text("Authorize app"), button:has-text("Authorize"), [data-testid="OAuth_Consent_Button"]')
   if await btn.count() > 0:
       await btn.first.click()
       try:
           await popup.wait_for_event("close", timeout=10000)
       except:
           pass
   ```
2. **Fallback to Direct Entry via Email/Form:**
   If OAuth popup fails, Gleam allows direct form input (Name + Email) on task expansion. Type into the name and email fields and click "Save" / "Continue" before verifying social tasks.
