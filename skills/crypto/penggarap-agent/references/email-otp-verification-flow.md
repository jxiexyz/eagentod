# Email OTP / Magic Link Verification Flow

**CRITICAL:** Submitting an email form is NOT completion. If the page shows "Check your email", "Enter code", "Verify", or any OTP input after email submission, you MUST complete the verification.

## Steps

### Step 1: Wait for email delivery
After submitting email on the site, wait 5 seconds: `sleep 5`

### Step 2: Fetch OTP or magic link via IMAP
```bash
python3 gmail.py "junamkaudek@gmail.com" "wmns ahle lybh hcqf" otp "domain_keyword"
```
Replace `domain_keyword` with sender/subject match (e.g. "loafmarkets", "takeapeak", "coinbase").

For magic links instead of OTP:
```bash
python3 gmail.py "junamkaudek@gmail.com" "wmns ahle lybh hcqf" link "domain_keyword"
```

### Step 3: Retry if not found
If `No matching email found`, retry up to 3 times with 10s delays:
```bash
sleep 10 && python3 gmail.py "junamkaudek@gmail.com" "wmns ahle lybh hcqf" otp "domain_keyword"
```

### Step 4: Submit the OTP or open the link
- **OTP:** Paste into the input field via `browser_type`. For React 6-box OTP inputs, type into the FIRST box only — it auto-populates the rest. If stuck, read `references/react-otp-input-bypass.md`.
- **Magic Link:** `browser_navigate` to the link URL.

### Step 5: Verify final success
Verify the final success page (e.g. "Welcome", "You're verified", dashboard). Only THEN report ✅.

## FORBIDDEN
- Reporting ✅ after just submitting email. "masukin email nunggu OTP" is NOT done.
- Skipping OTP verification because "email was sent".
- The anti-fraud guard in `post_topic42.py` will auto-reject reports containing "masukin email.*nunggu", "nunggu otp", "nunggu verif", etc.

## Tool Location
Script: `/home/ubuntu/.hermes/scripts/gmail.py` (also at skill `scripts/gmail.py`)
Credentials: from `airdrop_identity.py` main account.

## Timing Pitfalls
Read `references/imap-otp-timing-pitfalls.md` for Coinbase-specific OTP and timing details.
