# T-Rex (trex.xyz) OAuth Login Bug (Referral Modal Overlay)

**Issue**: `browser_click` or script clicks on OAuth buttons (Google/X) on `trex.xyz` fail with `subtree intercepts pointer events` or simply don't trigger the popup.

**Root Cause**: The login page (`/auth/portal-login`) forces a "Got a referral code?" modal overlay. It spans the entire screen (`<div class="fixed inset-0 ... z-50">`). Because the buttons (Google, X, etc.) are rendered *behind* this overlay (or the overlay intercepts all pointer events), standard Playwright/native clicks time out or click the overlay instead.

**Bypass / Fix**:
Before attempting to click any OAuth button, you MUST explicitly dismiss the referral modal via JavaScript injection using `evaluate()`.

```python
# 1. Dismiss the referral modal using JS evaluate (bypasses pointer interception)
await page.evaluate('''() => {
    const btns = Array.from(document.querySelectorAll('button'));
    const skipBtn = btns.find(b => b.innerText.includes("don't have a referral"));
    if(skipBtn) skipBtn.click();
}''')

await asyncio.sleep(2)

# 2. Click the OAuth button (also safer via evaluate to avoid lingering z-index issues)
await google_or_x_btn.evaluate('el => el.click()')
```

**Note**: The login page is typically loaded in a redirect iframe (`/auth/portal-login...`), so ensure you are operating on the correct page URL or frame context. Once the referral overlay is dismissed, the OAuth popups for Thirdweb (`embedded-wallet.thirdweb.com`) will trigger properly.