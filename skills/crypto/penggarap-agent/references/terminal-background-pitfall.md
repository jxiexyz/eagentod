# Terminal Backgrounding Pitfall

**Error:** `Foreground command uses '&' backgrounding. Use terminal(background=true) for long-lived processes...`

**Context:** When running persistent scripts like `wallet_connect.py --alive 120` or any daemon/server, you might be tempted to append a trailing `&` to the bash command (e.g., `python3 script.py &`) to let it run in the background.

**The Pitfall:** The Hermes `terminal` tool strictly prohibits using shell-level background wrappers (`&`, `nohup`, etc.) in foreground mode. This causes the tool to reject the command immediately with a status error. 

**The Solution:**
Do **not** use `&` in the `command` string. Instead, use the `terminal` tool's native background arguments:
1. Pass `background=true` in the tool call.
2. Pass `notify_on_complete=true` (unless it's an infinite watcher daemon).
3. Keep the command clean: `python3 ~/.hermes/scripts/wallet_connect.py --url "DOMAIN" --alive 120`

**Example Correct Tool Call:**
```json
{
  "command": "python3 ~/.hermes/scripts/wallet_connect.py --url \"domain.com\" --alive 120",
  "background": true,
  "notify_on_complete": true
}
```