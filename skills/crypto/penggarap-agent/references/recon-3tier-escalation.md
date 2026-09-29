# 3-Tier Reconnaissance Escalation

Before taking any action on a target, you MUST understand the page first.

**READ THE HINT FIRST.** If the script output includes `Hint: ...`, that text describes what the project wants. Use it to guide your recon.

## Tier 1 — `web_extract` (fastest, no browser needed)
Run `web_extract([url])` first. Returns full page as markdown. Enough to detect forms, buttons, wallet connect, social tasks, text content. If this gives you a clear picture of the task → skip to classification. ~90% of simple waitlist/email sites work here.

## Tier 2 — `lite_nav` + `lite_info` (lightweight browser)
If web_extract fails (Cloudflare, JS-heavy SPA, empty content), escalate:
`mcp_airdrop_tools_lite_nav(url)` → `mcp_airdrop_tools_lite_info()`. Returns buttons, inputs, page title. No images/CSS loaded — fast. Good for detecting interactive elements.
**CRITICAL PITFALL:** Do NOT use `lite_nav` for OAuth flows (like X.com or Google login). `lite_nav` uses an isolated session and does not have the authenticated cookies from the main CDP browser (port 9222). If you see X.com or OAuth links, jump straight to Tier 3 (CDP).

## Tier 3 — `browser_navigate` + `browser_snapshot(full=true)` (full CDP)
If Tier 1+2 both fail or site needs real JS interaction (React SPA, Web3 dApp, dynamic modals), use full browser:
`browser_navigate(url)` → `browser_snapshot(full=true)`. This renders everything including Shadow DOM, React state, wallet modals. Use this for actual interaction (clicking, typing, wallet connect).

## Rules
- Always start at Tier 1. Only escalate when the previous tier gives insufficient info.
- This saves browser resources and avoids unnecessary tab creation.
- After recon at ANY tier, classify the task type before proceeding.
- **DEAD SITE DETECTION:** If ANY tier returns 404, "Not Found", GoDaddy parking page, "Access Denied", or empty JSON error → site is DOWN. Report ❌ immediately with "situs mati/404". Do NOT escalate further or waste browser resources.
- **SPA DETECTION:** If Tier 1+2 return empty/minimal content but URL is valid → likely JS SPA. Jump to Tier 3. Do NOT report failure based on Tier 2 alone.
- **TMA/Mini App DETECTION:** If a Telegram bot responds with a WebApp/Mini App button → it requires Telegram Mini App (TMA) interaction. This CANNOT be automated via bot_automator.py. Report ❌ with "butuh Mini App TG, ga bisa diautomasin".

## Task Classification
After recon, classify:
- **Type A (Simple waitlist):** Email form → submit → done.
- **Type B (Email + OTP):** Email form → OTP/magic link sent → must verify via IMAP before done. READ `references/email-otp-verification-flow.md`.
- **Type C (Wallet connect):** Connect EVM/SOL wallet → sign message → done.
- **Type D (Social tasks):** Follow/Like/RT on X → verify on site → done.
- **Type E (Multi-step quest):** Combination of above. Complete ALL steps.

Key questions during classification:
- Does it require an EVM address?
- Is there a "Withdraw" or "Claim" button that requires a minimum balance?
- Does it use OAuth verification or just simple link clicks?
- Does it send an email verification after signup?

Formulate a step-by-step plan in your reasoning before clicking anything.
