# Zombie Lock & CDP Tab Cleanup Pitfalls

**The Problem:**
Workers connect to local CDP (`port 9222`). If the LLM crashes (OOM, timeout) while holding the browser lock (`/tmp/hermes_browser.lock`), the lock becomes a "zombie". 
The default cron cleanup script (`cleanup_tabs.py`) used `check_browser_busy()` which only checks if the lock file exists. It sees the zombie lock, assumes the browser is busy, skips cleanup, and leaves memory-hogging tabs hanging forever.

**The Fix:**
Cleanup scripts MUST use `acquire_browser_lock(timeout=5)`. 
1. If the worker is truly alive, it holds the lock and `acquire` fails after 5s -> cleanup skips gracefully (no collision).
2. If the lock is a zombie, `acquire_browser_lock` detects the dead PID, deletes the stale lock file, acquires a new lock, and proceeds to kill the hanging tabs.

```python
# RIGHT: Auto-heals zombie locks
from browser_lock import acquire_browser_lock, release_browser_lock

try:
    acquire_browser_lock(timeout=5, job_name="cleanup-tabs")
except RuntimeError:
    print("Browser actively in use. Skipping.")
    return
try:
    # ... close tabs ...
finally:
    release_browser_lock()

# WRONG: Gets permanently blocked by zombie locks
from browser_lock import check_browser_busy

if check_browser_busy():
    print("Browser busy. Skipping.")
    return
# ... close tabs ...
```