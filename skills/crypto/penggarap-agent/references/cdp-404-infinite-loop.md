# CDP 404 Connection Errors (Playwright/Browserbase)

When Playwright returns `Browserbase CDP error 404` or `CDP browser error 404 Not Found`, the connection to the specific CDP target (or the Chromium instance itself) is dead, corrupted, or pointing to a non-existent URL.

## The Pitfall
Because the airdrop worker reads from a queue (Topic 31 database), a CDP 404 error usually crashes the worker script *before* it can mark the project as failed in `worker_done.json`. 
When the cron job restarts the worker, it pulls the exact same project from the top of the queue, crashes again with the same 404, and enters an infinite crash loop. The background browser lock (`WORKER_CAN_RUN=true`) may also get stuck.

## The Fix
You must break the loop by manually marking the offending projects as failed so the precheck script skips them.

1. **Find the failing projects** (e.g., from Telegram logs or script output).
2. **Add them to `worker_done.json`** under the `failed` array.

```python
# Example update script (update_worker.py)
import json

def update_worker_done():
    path = "/home/ubuntu/.hermes/airdrop_data/worker_done.json"
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except:
        data = {"done": [], "failed": []}
        
    # Add the exact names from the queue (including the Msg ID part)
    projects = ["voice.fun (Msg 856)", "hood-ai.top (Msg 853)"]
    for project in projects:
        if project not in data.get("done", []) and project not in data.get("failed", []):
            data.setdefault("failed", []).append(project)
        
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

update_worker_done()
```

3. **Check the background lock**
If `momo_worker_wrapper.py` is used, the lock might be held. Wait for it to expire, or verify it released correctly after the script crashed. (The lock wrapper typically checks `browser_lock.py` logic).