# Event-Driven Worker Architecture

## The Problem
A purely cron-driven worker (e.g., running every 30m) introduces latency. Users dropping airdrop links into a Telegram channel expect immediate processing, but the cron job sits idle until its next scheduled tick.

If the main Hermes assistant is left in the channel to provide immediate response, it will auto-trigger on the link and attempt to process the task *as the chatbot*, causing tool-use logs to leak into the chat and conflicting with the designated worker bot.

## The Solution: Listener + Cron Sweeper

### 1. Isolate the Bots
- **Kick the main assistant bot** from the group. This entirely prevents the chatbot from auto-replying or triggering leaky tool-use operations on channel links.
- Use dedicated bot tokens for the **Researcher** (post to Topic 31) and the **Worker Reporter** (post to Topic 42).

### 2. Standalone Systemd Listener
Create a lightweight Telethon listener running as a `systemd` service (`topic31-listener.service`).
It listens for `NewMessage` events on the specific topic.
When an airdrop link is detected, it instantly kicks off the worker cron job via the CLI:
`subprocess.Popen(["/home/ubuntu/.local/bin/hermes", "cron", "run", "<worker_job_id>"])`
*(Pitfall: Ensure the absolute path to `hermes` is used, as `systemd` environments lack the user's `$PATH`)*.

### 3. Cron Sweeper Fallback
The worker agent itself remains a cron job (e.g., scheduled for `30 * * * *`).
- The listener handles the "immediate" event-driven execution.
- The cron schedule acts as a fallback/sweeper to process any tasks that were missed if the listener was temporarily down or the Telegram API failed.

### 4. Over-Engineering Restraints
Because the event-driven worker executes autonomously via LLM, it must be constrained from aggressive problem-solving loops:
- It will write raw Python/Playwright scripts to bypass headless browser failures.
- It will use `curl` and `grep` on `.js` bundles to reverse-engineer React SPA endpoints if the DOM is empty.
To prevent this, strictly define the allowed tools in the prompt and explicitly forbid `curl` and custom Python script creation.