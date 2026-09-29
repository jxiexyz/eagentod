**CRITICAL WARNING FOR WORKER RUNS (CDP SUPERVISOR):**
If you are running an active airdrop sequence via `browser_navigate` / `mcp_airdrop_tools_lite_nav` and hit a CDP crash (`ECONNREFUSED` or tunnel errors), **DO NOT attempt to manually restart Chromium using the steps below.** Doing so will desynchronize the Hermes CDP Supervisor, causing irreversible `HTTP error: 404 Not Found` errors for the rest of the run (see `references/cdp-supervisor-stale-404-pitfall.md`).
**Action:** Fast-fail the current target with category `SOFT_BLOCK_EXHAUSTED` and exit. Let the external cron environment cleanly reset the supervisor.

---

If you are debugging interactively (NOT mid-run) and Chrome CDP (port 9222) encounters persistent `SingletonLock` issues, it usually means the Chrome profile is locked by a previous process that didn't shut down cleanly, or there's a permission problem with the user data directory.

**Troubleshooting Steps:**

1.  **Kill all Chrome/Chromium processes:**
    ```bash
    pkill -f chrome
    pkill -f chromium
    ```
    (Note: `pkill chromium` might return exit code 1 if no chromium processes are running, which is normal).

2.  **Remove the `SingletonLock` file:**
    ```bash
    rm -f /home/ubuntu/.config/google-chrome/SingletonLock
    ```
    If `Permission denied` persists, check the permissions of `/home/ubuntu/.config/google-chrome` and its parent directories.

3.  **Attempt to restart Chromium:**
    First, verify which binary is available (`which chromium` vs `which chromium-browser`). If `/snap/bin/chromium` fails to bind or start, use `/usr/bin/chromium-browser` instead:
    ```bash
    /usr/bin/chromium-browser --remote-debugging-port=9222 --user-data-dir=/home/ubuntu/.config/google-chrome --no-sandbox --disable-dev-shm-usage --headless=new --start-maximized
    ```
    *(Note: Always run the browser process using `terminal(background=true)` and verify it works with `sleep 3; curl -s http://localhost:9222/json/version` in a separate command).*
    Use `--headless=new` for a new headless mode, and `--start-maximized` to ensure the window is large enough for content to render.

**Common Error Signals:**

-   `connect ECONNREFUSED ::1:9222`: The CDP server is not running or not accessible.
-   `Failed to create a ProcessSingleton for your profile directory`: Another instance of Chrome is running and holding the lock, or the lock file is corrupted/inaccessible.
-   `Permission denied (13)` on `SingletonLock`: Indicates a permissions issue with the profile directory.
