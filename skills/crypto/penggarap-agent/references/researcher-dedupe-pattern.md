# Researcher Cron: Deduplication & Context Window Limits

When a cron job acts as a researcher (scanning Telegram channels or feeds and passing data to an LLM for formatting), truncating the scraped text too heavily before sending it to the LLM will destroy the context needed for accurate filtering.

## The Bug
If you truncate a post to only its first line (e.g., `text.split('\n')[0][:120]`), the LLM only sees the title and the link. It cannot accurately evaluate if the link is a legitimate airdrop, an ad, or a scam, leading to garbage links passing the filter.

## The Fix
1. **Send Full Context (safely):** Pass a larger chunk of the post (e.g., `text.replace('\n', ' ')[:400]`) to the LLM so it can read the actual description and rules.
2. **Strict Evaluation Prompts:** Explicitly command the LLM to evaluate the post against the full context: *"EVALUASI SETIAP POST! JANGAN ASAL AMBIL LINK. FILTER LOW/MEDIUM RISK SAJA. JIKA POST ADALAH IKLAN, BERITA, ATAU SCAM, ABAIKAN!"*
3. **Use a Capable Model:** For filtering tasks requiring nuance (distinguishing real quests from ads), use `ag/gemini-pro-agent` or an equivalent strong reasoning model rather than a lightweight model (`gc/gemini-2.5-flash-lite`), as the lightweight model may aggressively rubber-stamp anything that looks like a URL.