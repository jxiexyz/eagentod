# Cloudflare Turnstile: invalid-input-response

**Symptom:**
When submitting a form (like email registration) that includes a Cloudflare Turnstile widget (`Verify you are human` checkbox in an iframe), clicking the Submit button without a valid Turnstile token results in an error message on the page:
`captcha protection: request disallowed (invalid-input-response)`

**Why it happens:**
- Headless browsers often fail Turnstile silently.
- Using `universal_bypass.js` removes the `disabled` attribute on the Submit button, but it **cannot** solve the Turnstile cryptography.
- Forcing the frontend button click just leads to a backend rejection because the Turnstile token payload is missing/invalid.

**Action:**
1. DO NOT try to brute-force or use `universal_bypass.js` to check the Turnstile box. It will not generate a valid token.
2. DO NOT retry with different emails/passwords. It is a hard block.
3. If an OAuth alternative (Google/X) exists on the same page, try it. If OAuth also fails (e.g., requires fresh manual login in a headless context), report as a hard block: `❌ [Domain] - Cloudflare Turnstile block (invalid-input-response) di form email, OAuth headless gagal.`
