# Telethon SQLite Database Lock Pitfall

## Symptom
When running a Telegram bot script (e.g., `bot_automator.py` or a custom `python3 -c` Telethon snippet), you encounter an error like:
`sqlite3.OperationalError: database is locked`

## Root Cause
The `~/.hermes/tg_new.session` file (which acts as a SQLite database for Telethon) is currently opened and locked by another Python process. This typically happens if a previous background script (like `bot_automator.py`) timed out, hung, or was backgrounded (`terminal(background=true)`) without properly disconnecting the client, leaving the process holding the file descriptor open.

## Resolution
1. Find the hanging process holding the lock on the session file:
   `lsof ~/.hermes/tg_new.session`
2. Note the PID from the `lsof` output.
3. Kill the process forcefully:
   `kill -9 <PID>`
   (Or use `pkill -f <script_name>` if you know the exact command line).
4. Rerun your Telethon script. It will now acquire the SQLite lock successfully.
