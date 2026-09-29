# Playwright Multi-Tab OAuth Handling

When executing airdrops via native CDP or Playwright, clicking "Login with Discord" or "Login with X" often opens a new tab. If the main script stays focused on the original page, it will hang or fail to detect the authorization button.

## The Challenge
The worker is attached to `contexts[0]`. When an OAuth button is clicked, a new `Page` object is spawned in that context, but the script's reference `page` still points to the old tab.

## Solution: Scanning and Authorizing
If an OAuth popup is suspected (or detected), use a utility function to scan all open tabs in the context, find the one with the authorization prompt, click it, and wait for it to close.

### Playwright Python Implementation

```python
async def handle_oauth_popups(context):
    """Scan all open pages in the context and click Authorize/Approve if found."""
    for p in context.pages:
        title = await p.title()
        url = p.url
        
        if "discord.com/oauth2" in url or "Discord" in title:
            try:
                # Discord uses "Authorize"
                btn = p.locator('button:has-text("Authorize")')
                if await btn.count() > 0:
                    await btn.click(timeout=3000)
                    # Wait for tab to auto-close after auth
                    await p.wait_for_event("close", timeout=10000)
            except:
                pass
                
        elif "api.x.com/oauth" in url or "twitter.com/oauth" in url or "oauth2/authorize" in url:
            try:
                # X/Twitter uses "Authorize app", "Authorize", or specific testid
                btn1 = p.locator('button:has-text("Authorize app")')
                btn2 = p.locator('button:has-text("Authorize")')
                btn3 = p.locator('[data-testid="OAuth_Consent_Button"]')
                
                btn = None
                if await btn1.count() > 0: btn = btn1
                elif await btn2.count() > 0: btn = btn2
                elif await btn3.count() > 0: btn = btn3
                
                if btn:
                    await btn.click(timeout=3000)
                    # The tab might close or just navigate away
                    try:
                        await p.wait_for_event("close", timeout=10000)
                    except:
                        await p.wait_for_url(lambda u: "oauth2/authorize" not in u, timeout=10000)
            except:
                pass
                
        elif "accounts.google.com" in url:
            try:
                # Google OAuth: Account selector or Continue button
                btn1 = p.locator('div[data-email]') # Select account row
                btn2 = p.locator('button:has-text("Continue")')
                btn3 = p.locator('span:has-text("Continue")')
                btn4 = p.locator('div[jsname="paFcre"]') # Google Material Next button
                
                btn = None
                if await btn1.count() > 0: btn = btn1.first
                elif await btn2.count() > 0: btn = btn2
                elif await btn3.count() > 0: btn = btn3
                elif await btn4.count() > 0: btn = btn4
                
                if btn:
                    await btn.click(timeout=3000)
                    try:
                        await p.wait_for_event("close", timeout=10000)
                    except:
                        pass
            except:
                pass
```

### Hermes Native Browser Implementation
If running as a native Hermes cron job using `browser` tools, you can switch focus by looking at `browser_snapshot()` output (which indicates if multiple tabs are open) or by using custom Playwright scripts via `execute_code()` or `terminal()` when the native tools cannot switch tabs efficiently.