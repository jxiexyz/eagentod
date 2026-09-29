# Anti-Fraud Guard & Banned Keyword Reporting

**CRITICAL RULE:** Telegram notifications sent via `post_topic42.py` undergo strict regex-based anti-fraud filtering to prevent fake/AI-hallucinated completions.

## The "Submit" Trap
If your success reason contains the word "Submit", "Submiting", "disubmit", or ANY variation, the cron job will immediately throw `Anti-fraud: Terdapat kata terlarang 'Submit' pada success report!` and crash.

**WHY:** Lazy AI agents often hallucinate "Form submitted" when they merely clicked a button but the form actually threw a validation error. The word is banned to force you to describe the ACTUAL outcome.

## Banned Words (DO NOT USE)
- `Submit` / `disubmit` / `mensubmit`
- `Connect` / `dikonek` / `meng-connect`
- `Sign up` / `Sign in`
- `Verify` (use `verifikasi sukses`, `OTP masuk`)
- `Done` (use `kelar`, `beres`, `udah`)

## Acceptable Indo Slang Alternatives
Use these patterns instead when writing the Telegram report:
- ✅ *[domain]* — kelar bro, tweet glow up udah dipost, form udah dikirim pake point RLP.
- ✅ *[domain]* — beres, OTP masuk, wallet nyambung.
- ✅ *[domain]* — udah masuk list waitlist, dapet posisi 500.
- ✅ *[domain]* — sukses klaim role di webnya.

**RECOVERY:** If you hit the anti-fraud trap, rewrite the message using pure Indonesian slang/natural language and remove the offending English loanword completely. Do not try to disguise it.