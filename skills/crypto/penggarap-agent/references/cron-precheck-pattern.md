# Cron LLM Silence / Idle Polling Pitfall

**The Problem:**
When a Hermes cron job wraps a python script that outputs a queue of tasks (e.g., `get_topic31.py`), and the queue is empty, the LLM will still run if the cron job is configured with `no_agent: false`. The prompt executes, the model reasons "there is nothing to do", and typically responds with `[SILENT]`.

While functional, this wastes tokens (the entire skill SOP context is sent to the LLM every tick, e.g. every 15m) and invites prompt-compliance issues (the model might accidentally respond with `[SILENT]` even when there are items, or ignore the silent instruction and output chatter).

**The Solution:**
Decouple the data-fetching from the LLM execution using a precheck script set in the cron job's `script` field.

```python
# worker_precheck.py
import sys
links = get_links()

if not links:
    # Exit silently. The cron supervisor sees empty stdout
    # and halts the run entirely. The LLM is NEVER invoked.
    sys.exit(0)

# If links exist, print them. The cron supervisor injects
# this stdout into the LLM's context window.
for name, url in links[:3]: # Cap execution to prevent iteration limit
    print(f"**{name}**\\n{url}")
```

In the cron job definition:
- Set `script: worker_precheck.py`
- Keep `no_agent: false`

**Why this matters:**
This architectural pattern saves massive amounts of tokens for event-driven workers that poll frequently but only act occasionally. It also prevents the agent from hitting max iteration limits by allowing the precheck script to cap the batch size (e.g. `links[:3]`) handed to the LLM per cycle.