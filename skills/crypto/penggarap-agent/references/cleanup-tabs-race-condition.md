# cleanup_tabs.py Race Condition Analysis (Jul 2026)

## Components
| Cron | Schedule | Lock | Behavior |
|------|----------|------|----------|
| `cleanup-chromium-tabs` | every 30m | ✅ acquire, skip if held | Close all non-x.com tabs (no args) |
| `momo-worker-agent` | every 15m | ❌ (Hermes native browser tools) | Per-project: `--url-pattern domain` only |

## Why No Collision
- Both cleanup paths use `browser_lock.py` (file-based, `/tmp/hermes_browser.lock`)
- Cleanup cron: timeout 5s → if lock held, prints "Browser actively in use" and returns
- Worker per-project cleanup: `--url-pattern [domain]` → only closes tabs matching that domain
- Hermes native `browser_navigate`/`browser_click` do NOT acquire lock, but this is OK:
  - Cleanup cron skips if lock held (by worker's own cleanup call)
  - Worst case: cleanup cron closes worker's active tab → worker retries via auto-recovery (Section 4)

## Bug Fixed
`cleanup_tabs.py` previously had NO argparse. `--url-pattern` and `--max-age` were silently ignored.
Worker calling `cleanup_tabs.py --url-pattern sweep.haus --max-age 0` actually closed ALL tabs.
Fix: added argparse, filter logic in cleanup loop. Verified live against CDP 9222.

## If Script Gets Overwritten
Worker LLM sometimes overwrites scripts during "debugging". If cleanup_tabs.py loses argparse:
1. Check `python3 cleanup_tabs.py --help` — should show `--url-pattern` and `--max-age`
2. If missing, restore from this reference or git history
