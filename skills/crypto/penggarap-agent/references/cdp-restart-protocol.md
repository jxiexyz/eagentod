# Restarting the CDP Browser Session correctly
When the CDP browser (`chrome` running with `--remote-debugging-port=9222`) crashes, it must be restarted via the designated startup scripts.

**Crucial Steps for CDP Restarts:**
1. **Kill Zombies:** Cleanly kill all orphaned chrome/chromium instances: `pkill -9 chrome && pkill -9 chromium`.
2. **Launch via Wrapper:** Use `bash /home/ubuntu/start-chromium-cdp.sh` via `terminal(background=true)`.
   - **DO NOT** attempt to run it in the foreground or assume the script is named `start_cdp.sh` in `.hermes/scripts/`.
3. **Wait & Verify:** Allow a moment for the websocket to bind, then check status via: `sleep 5 && curl -sSL http://localhost:9222/json/version`.
4. **Fallback:** If the wrapper script succeeds but the port refuses connections, kill `Xvfb` manually (`pkill -f Xvfb`) and run the Chromium command directly via `terminal(background=true)`:
   `/snap/bin/chromium --remote-debugging-port=9222 --user-data-dir=/home/ubuntu/chrome-profile --no-sandbox --disable-dev-shm-usage --disable-gpu --start-maximized --no-first-run --disable-session-crashed-bubble`

**Pitfall in Cron Context:**
- Running wrapper scripts via `terminal(command=...)` in a way that backgrounds them but closes the pty can kill the process. Use `terminal(command=..., background=true)` for scripts designed to run daemons.
