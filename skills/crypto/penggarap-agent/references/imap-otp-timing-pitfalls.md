# IMAP OTP Timing & Fetching Pitfalls

When an airdrop flow (like Coinbase Smart Wallet or Privy) requires email verification:

1. **Tool to Use:** Do NOT use `templates/gmail-otp-extractor.js` (it often throws MODULE_NOT_FOUND). Use the native Python script instead:
   `python3 ~/.hermes/scripts/imap_reader.py "<email>" "<app_password>" "<sender_email>"`

2. **Timing (CRITICAL):** Email delivery is not instant. If `imap_reader.py` returns `No emails found.`, you MUST wait before retrying. 
   Do this: `sleep 5 && python3 ~/.hermes/scripts/imap_reader.py ...`

3. **Coinbase Wallet Specifics:**
   - The sender is `no-reply@info.coinbase.com`.
   - The React OTP input form usually has 6 separate textboxes. Click or type into the FIRST box (e.g., `browser_type(ref='@e4', text='123456')`) and it will automatically populate the remaining 5 boxes.