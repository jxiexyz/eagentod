# Futility of DOM Bypass on Cloudflare WAF Blocks

If `browser_snapshot` shows titles like `Attention Required! | Cloudflare`, `Sorry, you have been blocked`, or `Just a moment...`, the block is happening at the network/Edge WAF level.

**CRITICAL RULE:** Do NOT attempt to use `universal_bypass.js` or `focus_bypass.js` on these pages. 

DOM-based injection scripts are designed to unlock React states, disabled buttons, or hidden forms on a *successfully loaded* web app. They cannot bypass a Cloudflare firewall block because the real website DOM has not even been served to the browser. (The script will report "Injection & Unlock complete!" because it successfully ran on the Cloudflare error page, but this accomplishes nothing).

**Action:** If a target URL returns a hard Cloudflare block that `browser_navigate` and standard stealth cannot penetrate, immediately report the failure (e.g., `❌ Cloudflare block di [domain]`) and move to the next task. Do not waste cycles attempting JS injection on a Cloudflare error page.

## Action-Gated Turnstile (In-Page Iframes)
Cloudflare Turnstile doesn't always block the initial page load. Sometimes it appears dynamically *inside an iframe* when you attempt an action (e.g., clicking "Connect Wallet", "Claim", or "Sign up").
- **Symptom:** `browser_snapshot` shows an `Iframe "Widget containing a Cloudflare security challenge"` with a `checkbox "Verify you are human"` *after* clicking an action button.
- **Futility:** Clicking this Turnstile checkbox natively via CDP in headless mode almost always fails (it spins infinitely or resets). Do NOT attempt to inject wallet mocks or DOM bypasses. Treat this as a hard WAF block, report the failure immediately (e.g., `❌ Kena limit Turnstile pas click tombol di [domain]`), and move on.