# CDP Tab Cleanup Pitfalls

When running a background job to sweep idle tabs on a headless CDP browser:

1. **Avoid Worker Collisions**: Use a lock file mechanism (`browser_lock.py` -> `check_browser_busy()`) to skip cleanup if the primary worker (e.g., Momo Worker) is currently holding the lock. This prevents closing tabs right out from under an active job.
2. **Handle Hanging Worker Tabs**: Workers that fail/time out often fail to call `Target.closeTarget` (because the LLM aborted or hung). This leaves "work" tabs open indefinitely, eventually causing OOM on small VPS instances.
3. **Aggressive Sweeping**: Do not trust domain whitelists for work domains to keep tabs open indefinitely. A tab with a work URL (e.g., a quest site) that remains open while the lock is FREE is a dead/hanging tab from a failed run. Close it aggressively.
4. **Implementation**: Only skip tabs that are explicitly required to remain open across jobs (e.g., `x.com` for persistent login) or `about:blank`. For all other URLs, if the browser is NOT locked, close the tab and catch exceptions (`try/except await page.close()`).