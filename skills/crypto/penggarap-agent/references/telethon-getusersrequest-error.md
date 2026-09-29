# Telethon GetUsersRequest Error in Worker Reporting

**Symptom:**
When a worker cron tries to run `python3 /home/ubuntu/.hermes/scripts/post_topic42.py "❌/✅ [message]"`, it fails with:
`Failed to send: The key is not registered in the system (caused by GetUsersRequest)`

**Context:**
- The script `post_topic42.py` uses Telethon with a pre-authenticated session file (`tg_new.session`).
- The error indicates that the Telegram session is invalid, banned, or the API keys/hash combination is mismatched, or the session cannot resolve the target group entity (3818905785).
- Alternate scripts like `post_to_topic42.py` rely on Bot API tokens, which are globally masked (`***`) by log sanitizers and cannot be used as fallbacks.

**Resolution Protocol (Worker Rule):**
1. **Do not attempt to fix the Python script.** The issue is at the session/account level, not a code bug. Overwriting `post_topic42.py` will not restore the dead session.
2. **Do not attempt to use bot token fallbacks.** `post_to_topic42.py` is permanently dead.
3. **Graceful failure:** If reporting fails, log the failure by appending the project string (e.g., `"portal.abs.xyz (Msg 625)"`) to the `"failed"` array in `/home/ubuntu/.hermes/airdrop_data/worker_done.json` using a terminal command (e.g., Python `json` module).
4. Do not hang in a loop trying to restore the report. End the execution flow normally after cleanup.